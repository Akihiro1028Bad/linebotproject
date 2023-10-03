# 標準ライブラリ
import logging
from datetime import datetime, timedelta


# 外部ライブラリ
from googleapiclient.discovery import build
import pytz

# ローカルモジュール
from models import User
import massege
from app import app, line_bot_api
import google_auth
import EventConfirmation


def notify_all_users_tomorrow_events():
    """
    すべてのユーザの今日のGoogleカレンダーの予定を取得し、LINEメッセージで送信する。
    """
    with app.app_context():  # アプリケーションのコンテキストを作成
        # データベースからすべてのユーザを取得
        all_users = User.query.all()

        for user in all_users:
            user_id = user.line_user_id

            logging.debug(f"ユーザ情報を取得しました。lineID→{user.line_user_id},アクセストークン{user.google_access_token}," +
                          f"リフレッシュトークン{user.google_refresh_token}")

            # Google認証情報の取得
            credentials = google_auth.get_google_credentials_from_db(user)
            logging.debug(f"認証情報を取得しました")

            # 認証情報が存在しない場合
            if not credentials:
                logging.debug(f"ユーザ{user_id}の認証情報の取得に失敗")
                continue  # 認証情報がなければ次のユーザに移動

            # GoogleカレンダーAPIクライアントの構築
            service = build('calendar', 'v3', credentials=credentials)

            # 明日の日付範囲を取得 (JST)
            jst = pytz.timezone('Asia/Tokyo')
            tomorrow_start = jst.localize(
                (datetime.today() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0))
            tomorrow_end = jst.localize(
                (datetime.today() + timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999))

            # 指定された日の予定をすべて取得
            all_events = EventConfirmation.get_oneday_events(tomorrow_start, tomorrow_end, service)

            # lineメッセージを送信
            one_day_events_message_send(user_id, all_events, tomorrow_start, "明日")

    logging.info("すべてのユーザに今日の予定を送信しました")


def one_day_events_message_send(user_id, all_events, start_day, day_type):
    if all_events:
        # 予定を開始時間でソート
        all_events.sort(key=lambda x: EventConfirmation.parse_event_time(x['start'].get('dateTime',
                                                                                        x['start'].get('date'))))

        # 予定のFlexメッセージを作成してプッシュ
        line_bot_api.push_message(user_id,
                                  [massege.show_oneday_events_message(all_events, start_day, day_type),
                                   massege.everyday_message_night()])


def main():
    notify_all_users_tomorrow_events()


if __name__ == "__main__":
    main()
