# 標準ライブラリ
import logging
from datetime import datetime, timedelta
from collections import defaultdict

# 外部ライブラリ
from googleapiclient.discovery import build
from linebot import LineBotApi
from linebot.models import TextSendMessage, PostbackEvent, CarouselContainer, FlexSendMessage
import pytz

# ローカルモジュール
import config
import google_auth
import massege
from models import UserState, User


def show_today_event(event: PostbackEvent, line_bot_api: LineBotApi):
    """
    今日のユーザのGoogleカレンダーの予定を取得し、LINEメッセージで送信する。

    Args:
        event (PostbackEvent): LINEのポストバックイベント
        line_bot_api (LineBotApi): LINE bot API クライアント
    """

    user_id = event.source.user_id
    user = User.query.filter_by(line_user_id=user_id).first()
    user_state = UserState.query.filter_by(user_id=user_id).first()

    credentials = google_auth.get_google_credentials_from_db(user)

    # 認証情報がない場合、ユーザにGoogle認証を求める
    if not credentials:
        send_google_auth_request(event, line_bot_api, user_id)
        return

    # 今日の予定を取得し、LINEメッセージで送信
    send_today_events(event, line_bot_api, credentials)

    # user_stateをクリア
    UserState.user_state_clear(user_state)


def send_google_auth_request(event, line_bot_api, user_id):
    """Google認証リンクを生成してユーザに送信する"""
    auth_link = google_auth.generate_auth_url(user_id)
    message = TextSendMessage(text=f"下のリンクからGoogle認証を行ってください。\n{auth_link}")
    line_bot_api.reply_message(event.reply_token, message)


def send_today_events(event, line_bot_api, credentials):
    """今日のユーザのGoogleカレンダーの予定を取得し、LINEメッセージで送信する"""
    service = build('calendar', 'v3', credentials=credentials)

    # 今日の日付範囲を取得 (JST)
    jst = pytz.timezone('Asia/Tokyo')
    today_start = jst.localize(datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))
    today_end = jst.localize(datetime.today().replace(hour=23, minute=59, second=59, microsecond=999999))

    all_events = get_oneday_events(today_start, today_end, service)
    one_day_events_message_send(event, line_bot_api, all_events, today_start, "今日")


def show_tomorrow_event(event: PostbackEvent, line_bot_api: LineBotApi):
    """
    明日のユーザのGoogleカレンダーの予定を取得し、LINEメッセージで送信する。

    Args:
        event (PostbackEvent): LINEのポストバックイベント
        line_bot_api (LineBotApi): LINE bot API クライアント
    """

    user_id = event.source.user_id
    user = User.query.filter_by(line_user_id=user_id).first()
    user_state = UserState.query.filter_by(user_id=user_id).first()

    credentials = google_auth.get_google_credentials_from_db(user)

    # 認証情報がない場合、ユーザにGoogle認証を求める
    if not credentials:
        send_google_auth_request(event, line_bot_api, user_id)
        return

    # 明日の予定を取得し、LINEメッセージで送信
    send_tomorrow_events(event, line_bot_api, credentials)

    # user_stateをクリア
    UserState.user_state_clear(user_state)


def send_tomorrow_events(event, line_bot_api, credentials):
    """明日のユーザのGoogleカレンダーの予定を取得し、LINEメッセージで送信する"""
    service = build('calendar', 'v3', credentials=credentials)

    # 明日の日付範囲を取得 (JST)
    jst = pytz.timezone('Asia/Tokyo')
    tomorrow_start = jst.localize((datetime.today() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0))
    tomorrow_end = jst.localize((datetime.today() + timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999))

    all_events = get_oneday_events(tomorrow_start, tomorrow_end, service)
    one_day_events_message_send(event, line_bot_api, all_events, tomorrow_start, "明日")


def show_day_after_tomorrow_event(event: PostbackEvent, line_bot_api: LineBotApi):
    """
    明後日のユーザのGoogleカレンダーの予定を取得し、LINEメッセージで送信する。

    Args:
        event (PostbackEvent): LINEのポストバックイベント
        line_bot_api (LineBotApi): LINE bot API クライアント
    """

    user_id = event.source.user_id
    user = User.query.filter_by(line_user_id=user_id).first()
    user_state = UserState.query.filter_by(user_id=user_id).first()

    credentials = google_auth.get_google_credentials_from_db(user)

    # 認証情報がない場合、ユーザにGoogle認証を求める
    if not credentials:
        send_google_auth_request(event, line_bot_api, user_id)
        return

    # 明後日の予定を取得し、LINEメッセージで送信
    send_day_after_tomorrow_events(event, line_bot_api, credentials)

    # user_stateをクリア
    UserState.user_state_clear(user_state)


def send_day_after_tomorrow_events(event, line_bot_api, credentials):
    """明後日のユーザのGoogleカレンダーの予定を取得し、LINEメッセージで送信する"""
    service = build('calendar', 'v3', credentials=credentials)

    # 明後日の日付範囲を取得 (JST)
    jst = pytz.timezone('Asia/Tokyo')
    day_after_start = jst.localize((datetime.today() + timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0))
    day_after_end = jst.localize((datetime.today() + timedelta(days=2)).replace(hour=23, minute=59, second=59, microsecond=999999))

    all_events = get_oneday_events(day_after_start, day_after_end, service)
    one_day_events_message_send(event, line_bot_api, all_events, day_after_start, "明後日")


def show_day_custom_event(event: PostbackEvent, line_bot_api: LineBotApi):
    """
    指定された日のGoogleカレンダーの予定を取得し、LINEメッセージで送信する。

    Args:
        event (PostbackEvent): LINEのポストバックイベント
        line_bot_api (LineBotApi): LINE bot API クライアント
    """

    user_id = event.source.user_id
    user = User.query.filter_by(line_user_id=user_id).first()
    user_state = UserState.query.filter_by(user_id=user_id).first()

    credentials = google_auth.get_google_credentials_from_db(user)

    # 認証情報がない場合、ユーザにGoogle認証を求める
    if not credentials:
        send_google_auth_request(event, line_bot_api, user_id)
        return

    # 指定された日の予定を取得し、LINEメッセージで送信
    send_custom_day_events(event, line_bot_api, credentials)

    # user_stateをクリア
    UserState.user_state_clear(user_state)


def send_custom_day_events(event, line_bot_api, credentials):
    """指定された日のユーザのGoogleカレンダーの予定を取得し、LINEメッセージで送信する"""
    service = build('calendar', 'v3', credentials=credentials)
    jst = pytz.timezone('Asia/Tokyo')

    date_str = event.postback.params["date"]
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    start = jst.localize((date_obj.replace(hour=0, minute=0, second=0, microsecond=0)))
    end = jst.localize(date_obj.replace(hour=23, minute=59, second=59, microsecond=999999))

    all_events = get_oneday_events(start, end, service)
    one_day_events_message_send(event, line_bot_api, all_events, start, "その他")


def show_week_events(event: PostbackEvent, line_bot_api: LineBotApi):
    """
        一週間の予定を示すFlexメッセージを送信する

        Args:
            event: PostbackEvent
            line_bot_api: LineBotApi
        """

    user_id = event.source.user_id
    user = User.query.filter_by(line_user_id=user_id).first()
    user_state = UserState.query.filter_by(user_id=user_id).first()

    # Google認証情報の取得
    credentials = google_auth.get_google_credentials_from_db(user)
    logging.debug("認証情報を取得")

    # 認証情報が存在しない場合
    if not credentials:
        logging.debug("認証情報の取得に失敗")
        # 認証リンクを生成してユーザに送信
        auth_link = google_auth.generate_auth_url(user_id)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=f"下のリンクからGoogle認証を行ってください。\n{auth_link}"))
        return

    # GoogleカレンダーAPIクライアントの構築
    service = build('calendar', 'v3', credentials=credentials)

    # 今日の日付範囲を取得 (JST)
    jst = pytz.timezone('Asia/Tokyo')
    today_start = jst.localize(datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))
    end = jst.localize((datetime.today() + timedelta(days=10)).replace(hour=23, minute=59, second=59,
                                                                             microsecond=999999))
    # 一週間分の予定を取得
    all_events = get_week_events(today_start,  end, service)

    # 日付ごとにイベントをグループ化するための辞書を初期化
    grouped_events = defaultdict(list)

    # イベントを日付ごとにグループ化
    for day_event in all_events:
        # イベントの開始時刻をJSTに変換
        start_time_str = day_event['start'].get('dateTime', day_event['start'].get('date'))
        start_datetime = datetime.fromisoformat(start_time_str).astimezone(pytz.timezone('Asia/Tokyo'))
        start_date = start_datetime.date()

        grouped_events[start_date].append(day_event)

    bubbles = []

    # 各日付のイベントをFlex Bubbleに変換
    for day, events in grouped_events.items():
        bubble = massege.create_day_bubble(events, day)
        bubbles.append(bubble)

    # カルーセルメッセージを作成
    carousel = CarouselContainer(contents=bubbles)

    line_bot_api.reply_message(event.reply_token,
                               [FlexSendMessage(alt_text="一週間の予定", contents=carousel),
                                massege.first_quick_reply()])

    UserState.user_state_clear(user_state)


def show_ask_date_picker(event: PostbackEvent, line_bot_api: LineBotApi):
    """
    ユーザに日付を選択してもらうためのDatePickerを表示します。

    Args:
        event (PostbackEvent): LINEのポストバックイベント
        line_bot_api (LineBotApi): LINE bot API クライアント
    """

    # ユーザIDを取得
    user_id = event.source.user_id

    # データベースから該当するユーザの情報を取得
    user = User.query.filter_by(line_user_id=user_id).first()

    # ユーザの現在の状態をデータベースから取得
    user_state = UserState.query.filter_by(user_id=user_id).first()

    # 日付を選択するためのメッセージをリプライ
    line_bot_api.reply_message(event.reply_token, massege.ask_for_date())

    # 次に適用する質問（日付選択）をユーザの状態として保存
    user_state.next_question = config.const_ask_date


def parse_event_time(event_time_str):
    jst = pytz.timezone('Asia/Tokyo')  # タイムゾーン情報
    try:
        # dateTime形式で解析
        return datetime.fromisoformat(event_time_str).astimezone(jst)
    except ValueError:
        # date形式で解析し、タイムゾーン情報を追加
        return jst.localize(datetime.strptime(event_time_str, '%Y-%m-%d'))


def get_oneday_events(start_day, end_day, service):

    start = start_day.astimezone(pytz.utc).isoformat()
    end = end_day.astimezone(pytz.utc).isoformat()

    # すべてのカレンダーから今日の予定を取得
    calendar_list = service.calendarList().list().execute()
    calendars = [calendar_entry['id'] for calendar_entry in calendar_list['items']]

    all_events = []
    for calendar_id in calendars:
        events_result = service.events().list(calendarId=calendar_id, timeMin=start,
                                              timeMax=end, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        for day_event in events:
            start_time_str = day_event['start'].get('dateTime', day_event['start'].get('date'))
            end_time_str = day_event['end'].get('dateTime', day_event['end'].get('date'))

            # 終日の予定の場合
            if 'date' in day_event['start']:
                start_date = datetime.fromisoformat(start_time_str).date()
                end_date = datetime.fromisoformat(end_time_str).date() - timedelta(days=1)  # 終日の終了日は次の日の0時なので、1日減らす

                # 開始日と終了日が今日でない場合はスキップ
                if start_date != start_day.date() or end_date != end_day.date():
                    continue

            all_events.append(day_event)

    return all_events


def get_week_events(start_day, end_day, service):
    # 開始日から10日後の日付を終了日とする
    start = start_day.astimezone(pytz.utc).isoformat()
    end = end_day.astimezone(pytz.utc).isoformat()

    # すべてのカレンダーから指定した期間の予定を取得
    calendar_list = service.calendarList().list().execute()
    calendars = [calendar_entry['id'] for calendar_entry in calendar_list['items']]

    all_events = []
    for calendar_id in calendars:
        events_result = service.events().list(calendarId=calendar_id, timeMin=start,
                                              timeMax=end, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        all_events.extend(events)

    logging.debug(f"all_events→1{all_events}")

    # 開始時刻がstart_dayよりも前のイベント（終日のイベントも含む）をフィルタリング
    jst = pytz.timezone('Asia/Tokyo')
    all_events = [event for event in all_events if
                  datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))).astimezone(
                      jst) >= start_day]

    logging.debug(f"all_events→1{all_events}")

    return all_events


def one_day_events_message_send(event: PostbackEvent, line_bot_api: LineBotApi, all_events, start_day, day_type):
    if not all_events:
        # 予定のFlexメッセージを作成してリプライ
        line_bot_api.reply_message(event.reply_token, [massege.not_event_message(),
                                                      massege.first_quick_reply()])

    else:
        # 予定を開始時間でソート
        all_events.sort(key=lambda x: parse_event_time(x['start'].get('dateTime', x['start'].get('date'))))

        # 予定のFlexメッセージを作成してリプライ
        line_bot_api.reply_message(event.reply_token,
                                   [massege.show_oneday_events_message(all_events, start_day, day_type),
                                    massege.first_quick_reply()])







