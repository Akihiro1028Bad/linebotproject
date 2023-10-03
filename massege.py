# 標準ライブラリ
import logging
import random
from datetime import datetime, timedelta, time

# 外部ライブラリ
import pytz
from linebot.models import (
    TextSendMessage, QuickReply, QuickReplyButton, MessageAction,
    PostbackAction, ButtonsTemplate, DatetimePickerTemplateAction, FlexSendMessage,
    BubbleContainer, CarouselContainer, TemplateSendMessage, DatetimePickerAction,
    BoxComponent, ButtonComponent, TextComponent, SeparatorComponent, URIAction
)

# ローカルモジュール
import config


logging.basicConfig(level=logging.DEBUG)

# -----------------------------------------基本メッセージ------------------------------------------------------------


def return_quick_reply():
    items = [
        QuickReplyButton(action=MessageAction(label="最初に戻る", text="最初に戻る"))
    ]

    # クイックリプライの設定
    quick_reply = QuickReply(items=items)

    return quick_reply





def first_quick_reply():
    items = [
        QuickReplyButton(action=MessageAction(label="予定の追加", text="予定の追加")),
        QuickReplyButton(action=MessageAction(label="予定の確認", text="予定の確認")),
        # QuickReplyButton(action=MessageAction(label="リマインド登録", text="リマインド登録"))
    ]

    messages = TextSendMessage(
        text="どの操作を行いますか？",
        quick_reply=QuickReply(items=items)
    )

    return messages


def begin_date_picker_template():

    buttons_template = ButtonsTemplate(
        text="予定の開始日時を設定しましょう！📅\n下のボタンから選んでください。",
        actions=[
            DatetimePickerTemplateAction(
                label="開始日時を選択",
                data="start_date_selected",
                mode="datetime"
            )
        ]
    )
    return buttons_template


def end_date_picker_template():
    buttons_template = ButtonsTemplate(
        text="予定の終了日時を設定しましょう！🕰️\n下のボタンから選んでください。",
        actions=[
            DatetimePickerTemplateAction(
                label="終了日時を選択",
                data="end_date_selected",
                mode="datetime"
            )
        ]
    )
    return buttons_template


def google_certification_success():
    # あらかじめ定義したテキストテンプレート
    text_template = ('''Google認証が完了しました！🎉\n
引き続き、私との会話を通じて以下のことが可能です。
✅ Googleカレンダーへの予定追加
✅ Googleカレンダーの予定のチェック\n
さらに、22時に翌日の予定をお知らせ。朝6時には当日の予定をお知らせします。\n
日々のスケジュール管理をよりスムーズに、より楽しくサポートさせていただきます！\n
どうぞよろしくお願い申し上げます😊''')

    # LINEへのメッセージ送信
    message1 = TextSendMessage(
        text=text_template
    )

    message2 = first_quick_reply()

    messages = [message1, message2]
    return messages


def message_auth_instruction(auth_url):
    """
    認証URLを含むボタンを作成します。
    :param auth_url: 認証URL
    """

    # ボタンテンプレートメッセージを作成
    buttons_template_message = TemplateSendMessage(
        alt_text='認証リンク',
        template=ButtonsTemplate(
            text='Googleアカウントで認証してください',
            actions=[
                URIAction(
                    label='認証ページへ',
                    uri=auth_url
                )
            ]
        )
    )

    return buttons_template_message

# -------------------------------------追加フロー-----------------------------------------------------------------------


def send_title():
    text = "次に予定の名前を具体的に入力してください📝\n例:「チームミーティング」\n\nやり直したい場合や最初に戻る場合は↓をタップしてね！"

    quick_reply = return_quick_reply()

    message = TextSendMessage(text=text, quick_reply=quick_reply)

    return message


def send_location():
    text = ("次に、イベントの場所を指定してください🌍\n"
            "「新宿駅」や「Sunny Cafe」のように具体的な名前や、\n"
            "Googleマップのリンクを共有しても大丈夫です✨")

    quick_reply = return_quick_reply()

    message = TextSendMessage(text=text, quick_reply=quick_reply)

    return message


def send_detail():
    text = ("イベントの詳細や必要事項を入力してください📝\n" +
            "また、参考となるURLがあれば添えて教えてください🔗\n" +
            "例:\n「持ち物: ノート、ペン✒️」\n「詳細URL: https://～～～～」")

    quick_reply = return_quick_reply()

    message = TextSendMessage(text=text, quick_reply=quick_reply)

    return message


def send_schedule_temp_confirmation(temp_event):
    text = (f"✨現在の入力内容✨\n"
            "📌【予定名】\n" +
            f"{temp_event.title}\n\n" +

            "⏱【開始日時】\n" +
            f"{temp_event.start_time.strftime('%Y年%m月%d日 %H時%M分')}\n\n" +

            "⏳【終了日時】\n" +
            f"{temp_event.end_time.strftime('%Y年%m月%d日 %H時%M分')}\n\n" +

            "🔍この内容で登録しますか？\n\n" +
            "予定の詳細（場所、メモ）の入力も可能です。\n" +
            "↓の選択からお選びください。")

    quick_reply = temp_confirmation_message()

    message = TextSendMessage(text=text, quick_reply=quick_reply)

    return message


def temp_confirmation_message():

    # クイックリプライのアイテム設定
    confirm_items = [
        QuickReplyButton(action=MessageAction(label="登録", text="登録")),
        QuickReplyButton(action=MessageAction(label="詳細を続けて入力", text="詳細を続けて入力")),
        QuickReplyButton(action=MessageAction(label="キャンセル", text="キャンセル"))
    ]

    # クイックリプライの設定
    quick_message = QuickReply(items=confirm_items)

    return quick_message


def send_schedule_confirmation(temp_event):
    text = (f"✨現在の入力内容✨\n"
            "📌【予定名】\n" +
            f"{temp_event.title}\n\n" +

            "⏱【開始日時】\n" +
            f"{temp_event.start_time.strftime('%Y年%m月%d日 %H時%M分')}\n\n" +

            "⏳【終了日時】\n" +
            f"{temp_event.end_time.strftime('%Y年%m月%d日 %H時%M分')}\n\n" +

            "📍【場所】\n" +
            f"{temp_event.location}\n\n" +

            "📝【メモ】\n" +
            f"{temp_event.note}\n\n" +

            "🔍この内容で登録しますか？")

    quick_reply = confirmation_message()

    message = TextSendMessage(text=text, quick_reply=quick_reply)

    return message


def confirmation_message():

    # クイックリプライのアイテム設定
    confirm_items = [
        QuickReplyButton(action=MessageAction(label="登録", text="登録")),
        QuickReplyButton(action=MessageAction(label="キャンセル", text="キャンセル"))
    ]

    # クイックリプライの設定
    quick_message = QuickReply(items=confirm_items)

    return quick_message

# ------------------------------------------------確認フロー-------------------------------------------------------------


def range_select_carousel():
    # 1枚目の内容
    # 1枚目の内容
    bubble_1 = BubbleContainer(
        body=BoxComponent(
            layout="vertical",
            contents=[
                # タイトル用のテキストコンポーネント
                TextComponent(text="予定の確認", weight="bold", size="xl"),

                # 説明文のテキストコンポーネント
                TextComponent(text="選択してください。", size="md", wrap=True),

                # セパレーターを追加してテキストとボタンを分ける
                SeparatorComponent(margin="md"),

                # ボタンを配置
                BoxComponent(
                    layout="vertical",
                    margin="md",  # セパレーターとボタンの間に余白を追加
                    contents=[
                        ButtonComponent(
                            style="secondary",
                            color="#DDDDDD",  # グレー
                            action=PostbackAction(label="今日の予定を確認", data="date=today"),
                            margin="sm"  # ボタン上部のマージンを追加
                        ),
                        ButtonComponent(
                            style="secondary",
                            color="#DDDDDD",  # グレー
                            action=PostbackAction(label="明日の予定を確認", data="date=tomorrow"),
                            margin="sm"  # ボタン上部のマージンを追加
                        ),
                        ButtonComponent(
                            style="secondary",
                            color="#DDDDDD",  # グレー
                            action=PostbackAction(label="明後日の予定を確認", data="date=day_after_tomorrow"),
                            margin="sm"  # ボタン上部のマージンを追加
                        )
                    ]
                )
            ]
        )
    )

    bubble_2 = BubbleContainer(
        body=BoxComponent(
            layout="vertical",
            contents=[
                # タイトル用のテキストコンポーネント
                TextComponent(text="予定の確認", weight="bold", size="xl"),

                # 説明文のテキストコンポーネント
                TextComponent(text="選択してください。", size="md", wrap=True),

                # セパレーターを追加してテキストとボタンを分ける
                SeparatorComponent(margin="md"),

                # ボタンを配置
                BoxComponent(
                    layout="vertical",
                    margin="md",  # セパレーターとボタンの間に余白を追加
                    contents=[
                        ButtonComponent(
                            style="secondary",
                            color="#DDDDDD",  # グレー
                            action=PostbackAction(label="今日から10日間の予定を確認", data="date=this_week"),
                            margin="sm"  # ボタン上部のマージンを追加
                        ),
                        ButtonComponent(
                            style="secondary",
                            color="#DDDDDD",  # グレー
                            action=PostbackAction(label="任意の日程の予定を確認", data="date=specific_date"),
                            margin="sm"  # ボタン上部のマージンを追加
                        )
                    ]
                )
            ]
        )
    )

    # カルーセルメッセージを作成
    carousel = CarouselContainer(contents=[bubble_1, bubble_2])  # 2枚目, 3枚目を ... の部分に追加

    flex_message = FlexSendMessage(
        alt_text="予定の確認",  # 代替テキスト
        contents=carousel,
        quick_reply=return_quick_reply()
    )
    return flex_message


def show_oneday_events_message(events, select_date, date_type):
    """
    一日の予定を示すFlexメッセージを生成する

    Args:
        events (list): イベントのリスト

    Returns:
        FlexSendMessage: 今日の予定のFlexメッセージ
        :param events:
        :param date_type:
        :param select_date:
    """
    # 曜日の名前を持つリストを定義
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]

    if date_type == "今日":
        date_text = "今日"
        # dayから曜日を取得
        weekday_str = weekdays[datetime.now().weekday()]
        day = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%m月%d日')

    elif date_type == "明日":
        date_text = "明日"
        weekday_str = weekdays[(datetime.now(pytz.timezone('Asia/Tokyo')) + timedelta(days=1)).weekday()]
        day = (datetime.now(pytz.timezone('Asia/Tokyo')) + timedelta(days=1)).strftime('%m月%d日')
    elif date_type == "明後日":
        date_text = "明後日"
        weekday_str = weekdays[(datetime.now(pytz.timezone('Asia/Tokyo')) + timedelta(days=2)).weekday()]
        day = (datetime.now(pytz.timezone('Asia/Tokyo')) + timedelta(days=2)).strftime('%m月%d日')
    else:
        date_text = select_date.strftime('%m月%d日')
        weekday_str = weekdays[select_date.weekday()]
        day = select_date.strftime('%m月%d日')

    # メッセージの初期の日付の表示を作成
    event_contents = [
        TextComponent(text=f"{date_text}の予定", weight="bold", size="xl"),
        TextComponent(text=f"{day}({weekday_str})の予定です", size="md", wrap=True),
        SeparatorComponent(margin="md")
    ]

    # イベントの詳細を追加
    for event in events:
        summary = event.get('summary', 'タイトル未設定')

        start_jst = get_jst_time_from_utc(
            datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))))
        end_jst = get_jst_time_from_utc(datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date'))))

        # 終日のイベントかどうかを確認
        is_all_day_event = start_jst.time() == time(0, 0) and (
                    end_jst.time() == time(0, 0) or end_jst.time() == time(23, 59))

        # 終日の場合とそれ以外でイベントの時間の表示を変える
        if is_all_day_event:
            event_time_description = "終日"
            event_text_color = "#FF0000"  # 赤色
        else:
            event_time_description = f"{format_event_time(start_jst)}~ {format_event_time(end_jst)}"
            event_text_color = "#000000"  # 黒色（またはデフォルト）

        event_description = f"{event_time_description}\n{summary}"

        event_contents.extend([
            TextComponent(text=event_description, size="md", wrap=True, color=event_text_color),
            ButtonComponent(
                style="link",
                height="sm",
                action=URIAction(label="Googleカレンダーで詳細を確認", uri=event['htmlLink'])
            ),
            SeparatorComponent(margin="md")
        ])

    # Flexメッセージの作成
    bubble = BubbleContainer(
        body=BoxComponent(
            layout="vertical",
            contents=event_contents
        )
    )

    return FlexSendMessage(alt_text=f"一日の予定", contents=bubble)


def create_day_bubble(events, target_date):
    """
    各日の予定を示すFlex Bubbleを生成する

    Args:
        events: その日のイベントのリスト
        target_date: 対象の日付

    Returns:
        BubbleContainer: Flex Bubble
    """

    # 曜日の名前を持つリストを定義
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    weekday_str = weekdays[target_date.weekday()]
    day = target_date.strftime('%m月%d日')

    # メッセージの初期の日付の表示を作成
    event_contents = [
        TextComponent(text=f"{day}({weekday_str})の予定", weight="bold", size="xl"),
        SeparatorComponent(margin="md")
    ]

    logging.debug(f"bubbleを作成する処理に入りましたevents→{events}")

    if not events:
        event_contents.extend([
            TextComponent(text="予定登録なし", size="md", wrap=True),
            SeparatorComponent(margin="md")
        ])

    else:
        # イベントの詳細を追加
        for event in events:
            summary = event.get('summary', 'タイトル未設定')

            start_jst = get_jst_time_from_utc(
                datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))))
            end_jst = get_jst_time_from_utc(datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date'))))

            # 終日のイベントかどうかを確認
            is_all_day_event = start_jst.time() == time(0, 0) and (
                    end_jst.time() == time(0, 0) or end_jst.time() == time(23, 59))

            # 終日の場合とそれ以外でイベントの時間の表示を変える
            if is_all_day_event:
                event_time_description = "終日"
                event_text_color = "#FF0000"  # 赤色
            else:
                event_time_description = f"{format_event_time(start_jst)}~ {format_event_time(end_jst)}"
                event_text_color = "#000000"  # 黒色（またはデフォルト）

            event_description = f"{event_time_description}\n{summary}"

            event_contents.extend([
                TextComponent(text=event_description, size="md", wrap=True, color=event_text_color),
                ButtonComponent(
                    style="link",
                    height="sm",
                    action=URIAction(label="Googleカレンダーで詳細を確認", uri=event['htmlLink'])
                ),
                SeparatorComponent(margin="md")
            ])

    # Flex Bubbleの作成
    bubble = BubbleContainer(
        body=BoxComponent(
            layout="vertical",
            contents=event_contents
        )
    )

    return bubble


# 毎日メッセージ
def everyday_message_morning():

    selected_message = random.choice(config.messages)

    return TextSendMessage(text="本日の予定をお知らせします。")


def everyday_message_night():

    selected_message = random.choice(config.messages_night)

    return TextSendMessage(text="明日の予定をお知らせします。")


def not_event_morning_message():
    text = ("Googleカレンダー🗓をチェックしましたが、今日の予定がまだ空いているようです✨ " +
            "予定を登録すると、一日の動きをしっかりとキャッチアップ🚀できますよ！")

    message = TextSendMessage(text=text)
    return message

def not_event_night_message():
    text = ("Googleカレンダー🗓をチェックしましたが、明日の予定がまだ空いているようです✨ " +
            "予定を登録すると、一日の動きをしっかりとキャッチアップ🚀できますよ！")

    message = TextSendMessage(text=text)
    return message


def ask_for_date():

    date_picker_message = TemplateSendMessage(
        alt_text='日付を選択してください',
        template=ButtonsTemplate(
            text='どの日の予定を確認しますか？',
            actions=[
                DatetimePickerAction(
                    label='日付を選択',
                    data='selected_date',
                    mode='date'
                )
            ]
        )
    )

    return date_picker_message


def not_event_message():
    text = "指定された日には予定が登録されていません。\n最初に戻ります"

    message = TextSendMessage(text=text)

    return message


def format_datetime(date_str):
    """指定された日時文字列を日本のフォーマットで整形する"""
    if 'T' in date_str:
        dt = datetime.fromisoformat(date_str)
        formatted = dt.strftime('%m月%d日 %H時%M分')
    else:  # all-day events
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        formatted = dt.strftime('%m月%d日')

    # ゼロ埋めの削除
    formatted = formatted.replace('月0', '月').replace('日0', '日').replace('時0', '時')
    return formatted


def get_jst_time_from_utc(utc_time):
    """
    UTC時間をJST時間に変換する

    Args:
        utc_time (datetime): UTC時間

    Returns:
        datetime: JST時間
    """
    jst = pytz.timezone('Asia/Tokyo')
    return utc_time.astimezone(jst)


def format_event_time(event_time):
    """
    イベント時間を所定のフォーマットに変換する

    Args:
        event_time (datetime): イベント時間

    Returns:
        str: フォーマット済みのイベント時間
    """
    return event_time.strftime('%m/%d %H:%M')




