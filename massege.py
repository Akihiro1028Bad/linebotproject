from datetime import datetime, timedelta
from linebot.models import (TextMessage, MessageEvent, TextSendMessage, QuickReply, QuickReplyButton, MessageAction,
                            PostbackAction)
import logging

logging.basicConfig(level=logging.DEBUG)

# -----------------------------------------基本メッセージ------------------------------------------------------------


def completion_registration():
    # クイックリプライのアイテム設定

    items = [
        QuickReplyButton(action=MessageAction(label="予定の追加", text="予定の追加")),
        QuickReplyButton(action=MessageAction(label="予定の確認", text="予定の確認"))
    ]

    # クイックリプライの設定
    quick_reply = QuickReply(items=items)

    # 初回メッセージの設定
    quick_reply_message = TextSendMessage(
        text="予定の登録が完了しました。\n次は、何を手伝いましょうか？"
             ""
             ""
             ""
             ""
             ""
             ""
             "",
        quick_reply=quick_reply
    )
    return quick_reply_message


def confirmation_message():

    # クイックリプライのアイテム設定
    confirm_items = [
        QuickReplyButton(action=MessageAction(label="登録", text="登録")),
        QuickReplyButton(action=MessageAction(label="キャンセル", text="キャンセル"))
    ]

    # クイックリプライの設定
    quick_message = QuickReply(items=confirm_items)

    return quick_message


def cancel_message():
    # クイックリプライのアイテム設定
    items = [
        QuickReplyButton(action=MessageAction(label="予定の追加", text="予定の追加")),
        QuickReplyButton(action=MessageAction(label="予定の確認", text="予定の確認"))
    ]

    # クイックリプライの設定
    quick_reply = QuickReply(items=items)

    cansel_message = TextSendMessage(text="最初に戻りました。何をお手伝いしましょうか？$",
                                     emojis=[
                                         {
                                             "index": 22,
                                             "productId": "5ac21a18040ab15980c9b43e",
                                             "emojiId": "028"
                                         },
                                        ],
                                     quick_reply=quick_reply)
    return cansel_message


def first_message():
    # クイックリプライのアイテム設定

    items = [
        QuickReplyButton(action=MessageAction(label="予定の追加", text="予定の追加")),
        QuickReplyButton(action=MessageAction(label="予定の確認", text="予定の確認"))
    ]

    # クイックリプライの設定
    quick_reply = QuickReply(items=items)

    # 初回メッセージの設定
    quick_reply_message = TextSendMessage(
        text="予定の「予定の追加」「予定の確認」のどちらをおこないますか？$",
        emojis=[
            {
                "index": 30,
                "productId": "5ac223c6040ab15980c9b44a",
                "emojiId": "051"
            },
        ],
        quick_reply=quick_reply
    )
    return quick_reply_message


def month_more_message():

    # 本日の日付を取得（例: "2023-09-09"）
    today_date = datetime.now().strftime('%Y-%m-%d')
    # 明日の日付を取得（例: "2023-09-10"）
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    # あさっての日付を取得（例: "2023-09-11"）
    day_after_tomorrow = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')

    items = [
        QuickReplyButton(action=MessageAction(label="今日", text =today_date)),
        QuickReplyButton(action=MessageAction(label="明日", text=tomorrow_date)),
        QuickReplyButton(action=MessageAction(label="明後日", text=day_after_tomorrow)),
        QuickReplyButton(action=MessageAction(label="最初に戻る", text="最初に戻る"))
    ]

    # クイックリプライの設定
    quick_reply = QuickReply(items=items)

    text = TextSendMessage(text="選択された日には予定が登録されていません。\n" +
                                "再度確認する日を選択してください。", quick_reply=quick_reply)
    return text


def get_event_details_message(event):
    # クイックリプライのアイテム設定
    items = [
        QuickReplyButton(action=PostbackAction(label="この予定を削除する", data=f"delete_event:{event.id}")),
        QuickReplyButton(action=MessageAction(label="最初に戻る", text="最初に戻る"))
    ]

    # クイックリプライの設定
    quick_reply = QuickReply(items=items)

    message = (f"★予定内容★\n" +
               "【予定名】\n" +
               f"{event.title}\n\n" +

               "【開始日時】\n" +
               f"{event.start_time.strftime('%Y年%m月%d日 %H時%M分')}\n\n" +

               "【終了日時】\n" +
               f"{event.end_time.strftime('%Y年%m月%d日 %H時%M分')}\n\n" +

               "【場所】\n" +
               f"{event.location}\n\n" +

               "【メモ】\n" +
               f"{event.note}")

    text = TextSendMessage(text=message, quick_reply=quick_reply)
    return text

# -------------------------------------追加フロー-----------------------------------------------------------------------


def add_message(user_state, temp_event, cansel_text):
    if user_state == 'title':
        text = ("【予定の名前】を入力してください$\n" +
                "最初に戻る場合は↓を押す")

        logging.debug(f"user_state.next_question: {user_state}")
        logging.debug(f"text: {text}")
        return text

    if user_state == 'start_time':

        message = ("★現在の入力内容★\n" +
                   "【予定名】\n" +
                   f"{temp_event.title}\n\n" +
                   "-------------\n" +
                   "【予定の開始日時】を入力してください$\n\n" +
                   "(例)\n2023年1月1日12時0分の場合\n\n" +
                   "「202301011200」と入力\n\n" +
                   "最初に戻る場合は↓を押す")

        text = message
        return text

    if user_state == 'end_time':
        text = (
                "★現在の入力内容★\n" +
                "【予定名】\n" +
                f"{temp_event.title}\n\n" +

                "【開始日時】\n" +
                f"{temp_event.start_time.strftime('%Y年%m月%d日 %H時%M分')}\n\n" +

                "-------------\n" +
                "【予定の終了時間】を入力してください。\n\n " +
                "(例)\n2023年1月1日12時0分の場合\n\n" +
                "「202301011200」と入力\n\n" +
                "最初に戻る場合は↓を押す"
        )
        return text

    if user_state == 'location':

        text = (
                "★現在の入力内容★\n" +
                "【予定名】\n" +
                f"{temp_event.title}\n\n" +

                "【開始日時】\n" +
                f"{temp_event.start_time.strftime('%Y年%m月%d日 %H時%M分')} \n\n" +

                "【終了日時】\n" +
                f"{temp_event.end_time.strftime('%Y年%m月%d日 %H時%M分')}\n\n" +

                "-------------\n" +
                "【予定の場所】を入力してください。\n\n" +
                "最初に戻る場合は↓を押す"
        )
        return text

    if user_state == 'note':
        text = (
                "★現在の入力内容★\n" +
                "【予定名】" +
                f"{temp_event.title}\n\n" +

                "【開始日時】\n" +
                f"{temp_event.start_time.strftime('%Y年%m月%d日 %H時%M分')} \n\n" +

                "【終了日時】\n" +
                f"{temp_event.end_time.strftime('%Y年%m月%d日 %H時%M分')}\n\n" +

                "【場所】\n" +
                f"{temp_event.location}\n\n" +

                "-------------\n" +
                "【メモ】があれば入力してください。\n\n" +
                "最初に戻る場合は↓を押す"

        )
        return text

    if user_state == 'confirmation':
        text = (f"★現在の入力内容★\n"
                "【予定名】\n" +
                f"{temp_event.title}\n\n" +

                "【開始日時】\n" +
                f"{temp_event.start_time.strftime('%Y年%m月%d日 %H時%M分')}\n\n" +

                "【終了日時】\n" +
                f"{temp_event.end_time.strftime('%Y年%m月%d日 %H時%M分')}\n\n" +

                "【場所】\n" +
                f"{temp_event.location}\n\n" +

                "【メモ】\n" +
                f"{temp_event.note}\n\n" +

                "この内容で登録しますか？")
        return text

# ------------------------------------------------参照フロー-------------------------------------------------------------


def confirmation_sc_message(user_state):

    if user_state == "select_confirmation_date":
        # 本日の日付を取得（例: "2023-09-09"）
        today_date = datetime.now().strftime('%Y-%m-%d')
        # 明日の日付を取得（例: "2023-09-10"）
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        # あさっての日付を取得（例: "2023-09-11"）
        day_after_tomorrow = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')

        items = [
            QuickReplyButton(action=MessageAction(label="今日", text=today_date)),
            QuickReplyButton(action=MessageAction(label="明日", text=tomorrow_date)),
            QuickReplyButton(action=MessageAction(label="明後日", text=day_after_tomorrow)),
            QuickReplyButton(action=MessageAction(label="最初に戻る", text="最初に戻る"))
        ]

        # クイックリプライの設定
        quick_reply = QuickReply(items=items)

        text = TextSendMessage(text="確認する日を選択してください。\nまたは、「2023-01-01」の形式で入力してください"
                               , quick_reply=quick_reply)
        return text

    if user_state == 'select_year_answer':
        # 選択できる月のリストを作成する
        selectable_months = [str(month) for month in range(1, 13)]

        # クイックリプライボタンのリストを作成する
        items = [QuickReplyButton(action=MessageAction(label=f"{month}月", text=f"{month}")) for month in
                 selectable_months]

        # クイックリプライの設定
        quick_reply = QuickReply(items=items)

        text = TextSendMessage(text="参照したい「月」を選択してください。", quick_reply=quick_reply)

        return text

    if user_state == 'select_month':

        items = [
            QuickReplyButton(action=MessageAction(label="はい", text="はい")),
            QuickReplyButton(action=MessageAction(label="いいえ", text="いいえ"))
        ]

        quick_reply = QuickReply(items=items)

        text = TextSendMessage(text="「日」で絞りますか？",quick_reply=quick_reply)
        return text
