import logging

from flask import Flask
from flask_migrate import Migrate
from flask import request, abort

from linebot import LineBotApi, WebhookHandler

from linebot.models import TextMessage, MessageEvent, PostbackEvent, FollowEvent, TextSendMessage

from models import db
from EventHandler import EventHandler

import os

import auth

API_KEY = os.environ.get("API_KEY")
DATABASE_URI = os.environ.get("DATABASE_URI")
LINE_SECRET = os.environ.get("LINE_SECRET")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI  # SQLiteデータベースへのパス
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
    auth_url = auth.generate_auth_url()
    # 生成したリンクをユーザーに送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"Google認証を行うには、以下のリンクをクリックしてください: {auth_url}")
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    with app.app_context():  # アプリケーションコンテキストを設定
        db.create_all()  # ここでデータベースを作成
    app.run(debug=True)

