import logging

from flask import Flask
from flask_migrate import Migrate
from flask import request, abort


from google_auth_oauthlib.flow import Flow, InstalledAppFlow

from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from flask import redirect, url_for, request

from googleapiclient.discovery import build

from linebot import LineBotApi, WebhookHandler

from linebot.models import TextMessage, MessageEvent, PostbackEvent, FollowEvent, TextSendMessage

from models import db
from models import User
from EventHandler import EventHandler

import os

API_KEY = os.environ.get("API_KEY")
DATABASE_URI = os.environ.get("DATABASE_URI")
LINE_SECRET = os.environ.get("LINE_SECRET")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"  # SQLiteデータベースへのパス
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 変更を追跡しない設定
db.init_app(app)  # ここでdbオブジェクトを初期化
# Flask-Migrateを初期化
migrate = Migrate(app, db)


line_bot_api = LineBotApi(API_KEY)
handler = WebhookHandler(LINE_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        print("ハンドリング呼ばれてます")
        handler.handle(body, signature)
    except Exception as e:
        print("ハンドリング呼ブ時に何か起きてます", e)
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    try:
        eventhandler = EventHandler(event, line_bot_api)
        eventhandler.handle()

        print("メッセージ送信完了")
    except Exception as e:
        print("メッセージが送信できてない。エラー内容:", e)


@handler.add(PostbackEvent)
def handle_postback(event):
    # postbackのデータを取得
    data = event.postback.data
    eventhandler = EventHandler(event, line_bot_api)

    # dataの初めの部分（プレフィックス）を取得
    prefix = data.split(":")[0]

    if prefix == "event_details":
        eventhandler.get_event_details(data)

    if prefix == "show_events":
        # ここでhandle_next_page_requestメソッドを呼び出す
        eventhandler.handle_next_page_request(data)

    if prefix == "delete_event":
        eventhandler.delete_schedule(data)


@handler.add(FollowEvent)
def handle_follow(event):
    # Google認証のリンクを生成
    auth_url = generate_auth_url()
    # 生成したリンクをユーザーに送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"Google認証を行うには、以下のリンクをクリックしてください: {auth_url}")
    )


@app.route("/login", methods=['GET'])
def login():
    auth_url = generate_auth_url()  # Google認証ページへのURLを生成
    return redirect(auth_url)  # 生成したURLにリダイレクト


# Google OAuth2.0のフローを開始
@app.route('/login', methods=['GET'])
def generate_auth_url():
    """
    Googleの認証ページへのリダイレクトURLを生成する関数。
    実際にリダイレクトするのではなく、URLのみを返します。
    """
    try:
        flow = InstalledAppFlow.from_client_secrets_file('secrets/credentials.json',
                                                         scopes=['https://www.googleapis.com/auth/calendar'])

        # flow.redirect_uri = 'https://line-bot-oniisan-test-d81a1f540a61.herokuapp.com/oauth2callback'
        flow.redirect_uri = 'https://line-bot-oniisan-test-d81a1f540a61.herokuapp.com'
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        return authorization_url
    except Exception as e:
        logging.error(f"Error generating the auth URL: {e}")
        return None


# Googleからのリダイレクトをハンドル
@app.route('/oauth2callback', methods=['GET'])
def oauth2callback():
    """
    ユーザがGoogleの認証ページで認証を完了した後のリダイレクトURLを処理。
    Googleからの認証情報を受け取り、Google Calendar APIへのアクセスを可能にする。
    """
    user = None  # <-- ここでuserを初期化
    credentials = None
    user_email = None
    user_id = None
    try:
        state = request.args.get('state', '')

        flow = InstalledAppFlow.from_client_secrets_file(
            './secrets/credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar'],
            state=state
        )
        flow.redirect_uri = url_for('oauth2callback', _external=True)
        authorization_response = request.url
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)

        userinfo = service.people().get(userId='me').execute()
        user_email = userinfo.get('email')
        user_id = userinfo.get('id')

    except HttpError as e:
        if e.resp.status == 401:
            # トークンの有効期限が切れた場合の処理
            if not user:
                user = User.query.filter_by(google_email=user_email).first()

            if user:
                new_access_token, new_refresh_token = renew_token(user.google_refresh_token)
                credentials.token = new_access_token
                credentials.refresh_token = new_refresh_token
                user.google_access_token = new_access_token
                user.google_refresh_token = new_refresh_token
                db.session.commit()

                service = build('calendar', 'v3', credentials=credentials)
                userinfo = service.people().get(userId='me').execute()
            else:
                logging.error("User not found in the database.")
                return "User not found.", 400
        else:
            logging.error(f"Error while making a request to the Google API: {e}")
            return "Error making a request to Google API.", 500
    except Exception as e:
        logging.error("Unexpected error:", e)
        return "An unexpected error occurred.", 500

    # トークン更新後、またはエラーが発生しなかった場合の処理
    if not user:
        user = User.query.filter_by(google_email=user_email).first()
        if not user:
            User.add_new_user(google_email=user_email, google_user_id=user_id)

    # ... その他のAPIを使用した処理 ...

    return "Successfully authenticated and connected to Google Calendar."


def renew_token(refresh_token):
    """
    リフレッシュトークンを使用して新しいアクセストークンを取得します。
    """
    # 事前に保存していたクライアントIDとクライアントシークレットを使用してCredentialsオブジェクトを作成
    credentials = Credentials(
        None,  # アクセストークンはまだないのでNone
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id='223963817040-3h4pl5jrbedo1n148qckia9749vp89fu.apps.googleusercontent.com',
        client_secret='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'
    )

    # 新しいアクセストークンを取得
    request_object = Request()
    # 新しいアクセストークンを取得
    credentials.refresh(request_object)

    # 新しいアクセストークンとリフレッシュトークンを返す
    return credentials.token, credentials.refresh_token


if __name__ == '__main__':
    api_key = os.environ.get('API_KEY')
    print(api_key)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    with app.app_context():  # アプリケーションコンテキストを設定
        db.create_all()  # ここでデータベースを作成
    app.run(debug=True)

