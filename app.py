# 標準ライブラリ
import logging
from datetime import datetime, timedelta

# 外部ライブラリ
from flask import Flask, abort, request
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextMessage, MessageEvent, PostbackEvent,
    FollowEvent, UnfollowEvent
)
import requests

import config
# ローカルモジュール
import models
import google_auth
import EventConfirmation
from models import db
from EventHandler import EventHandler


DATABASE_URL = config.DATABASE_URL
logging.debug(f"データベースURL→{DATABASE_URL}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 変更を追跡しない設定
db.init_app(app)  # ここでdbオブジェクトを初期化
# Flask-Migrateを初期化
migrate = Migrate(app, db)

line_bot_api = LineBotApi(config.LINE_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_SECRET)


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
    """
    LINEからのテキストメッセージを処理する関数。
    """
    try:
        # メッセージを既読にする
        mark_message_as_read(event.source.user_id)

        # イベントハンドラを使用してメッセージを処理
        event_handler = EventHandler(event, line_bot_api)
        event_handler.handle()

        logging.debug("メッセージ送信完了")

    except Exception as e:
        logging.error(f"メッセージが送信できていない。エラー内容: {e}")


def mark_message_as_read(user_id):
    """
    LINEのメッセージを既読にする関数。
    """
    headers = {
        "Authorization": f"Bearer {config.LINE_ACCESS_TOKEN}"
    }

    endpoint = f"https://api.line.me/v2/bot/message/{user_id}/read"
    response = requests.post(endpoint, headers=headers)

    if response.status_code != 200:
        logging.error(f"Error marking message as read: {response.text}")


# ユーザーごとの最後のアクションタイムを追跡するディクショナリ
user_last_action = {}


@handler.add(PostbackEvent)
def handle_postback(event):
    """
    LINEからのポストバックイベントを処理する関数。
    """
    user_id = event.source.user_id  # ユーザーIDを取得

    # 現在のタイムスタンプを取得
    current_time = datetime.now()

    # ユーザーの最後のアクションタイムを取得（存在しない場合はデフォルト値として現在時刻の10秒前を使用）
    last_action_time = user_last_action.get(user_id, current_time - timedelta(seconds=10))

    # 最後のアクションから2秒未満の場合はイベントを無視
    if current_time - last_action_time < timedelta(seconds=5):
        print("Please wait for a while before pressing again")  # ここで適切な応答をLINEに送信
        return

    # 最後のアクションタイムを更新
    user_last_action[user_id] = current_time

    data = event.postback.data
    event_handler = EventHandler(event, line_bot_api)

    # dataに基づいて適切なアクションを実行
    if data.startswith("start_date_selected"):
        logging.debug("start_date_selectedを受け取りました")
        event_handler.begin_date_input()

    elif data.startswith("end_date_selected"):
        logging.debug("end_date_selectedを受け取りました")
        event_handler.finish_date_input()

    elif data == 'date=today':
        EventConfirmation.show_today_event(event, line_bot_api)

    elif data == 'date=tomorrow':
        EventConfirmation.show_tomorrow_event(event, line_bot_api)

    elif data == 'date=day_after_tomorrow':
        EventConfirmation.show_day_after_tomorrow_event(event, line_bot_api)

    elif data == 'date=this_week':
        EventConfirmation.show_week_events(event, line_bot_api)

    elif data == 'date=specific_date':
        EventConfirmation.show_ask_date_picker(event, line_bot_api)

    elif data == 'selected_date':
        EventConfirmation.show_day_custom_event(event, line_bot_api)


@handler.add(FollowEvent)
def handle_follow(event):
    """
    :param event: 友達追加時のイベント
    :return: URLを作成し、ユーザに見せる
    """
    google_auth.handle_follow(event, line_bot_api)


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    """
    LINEユーザーがボットをブロックしたときの処理。
    データベースから該当ユーザーと関連データを削除します。

    Args:
        event (UnfollowEvent): ブロックされたときのイベント
    """
    user_id = event.source.user_id
    logging.debug(f"ユーザがボットをブロックしました。ラインユーザID→{user_id}")

    try:
        # データベースから関連するデータを検索
        user_to_delete = models.User.query.filter_by(line_user_id=user_id).first()
        temp_event_delete = models.TempEvent.query.filter_by(user_id=user_id).first()
        user_state_delete = models.UserState.query.filter_by(user_id=user_id).first()

        # Userデータの削除
        if user_to_delete:
            models.db.session.delete(user_to_delete)
            logging.debug(f"ユーザデータを削除しました。ラインユーザID→{user_id}")

        # TempEventデータの削除
        if temp_event_delete:
            models.db.session.delete(temp_event_delete)
            logging.debug(f"テンプデータを削除しました。ラインユーザID→{user_id}")

        # UserStateデータの削除
        if user_state_delete:
            models.db.session.delete(user_state_delete)
            logging.debug(f"user_stateを削除しました。ラインユーザID→{user_id}")

        # データベースの変更をコミット
        models.db.session.commit()

    except Exception as e:
        logging.error(f"ユーザデータの削除中にエラーが発生しました。内容→{e}")


@app.route('/oauth2callback', methods=['GET', 'POST'])
def oauth2callback():
    result = google_auth.oauth2callback(line_bot_api)

    return result


if __name__ == '__main__':
    # ProxyFixの適用 (Herokuや他のプロキシサーバーでの運用時に必要)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

    # ログ設定
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # アプリケーションコンテキスト内でデータベースを初期化
    with app.app_context():
        db.create_all()

    # アプリケーションの実行
    app.run(debug=False)
