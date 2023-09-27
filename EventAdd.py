# 標準ライブラリ
import logging

# 外部ライブラリ
from linebot.models import TextSendMessage, MessageEvent

# ローカルモジュール
import config
import google_auth
import massege
from models import db, UserState, User, TempEvent


def event_add_question(event: MessageEvent, line_bot_api, user_state: UserState, temp_event: TempEvent):
    send_text = event.message.text

    handlers = {
        config.const_title_input_wait: handle_title_input,
        config.const_temp_confirmation_wait: handle_decision_or_continue,
        config.const_location_input_wait: handle_location_input,
        config.const_detail_input_wait: handle_detail_input,
        config.const_confirmation_wait: handle_confirmation
    }

    handler = handlers.get(user_state.next_question)
    if handler:
        handler(event, line_bot_api, user_state, temp_event, send_text)


def handle_title_input(event, line_bot_api, user_state, temp_event, send_text):
    temp_event.title = send_text
    db.session.commit()

    line_bot_api.reply_message(event.reply_token, [massege.send_schedule_temp_confirmation(temp_event)])

    user_state.next_question = config.const_temp_confirmation_wait
    db.session.add(user_state)
    db.session.commit()


def handle_decision_or_continue(event, line_bot_api, user_state, temp_event, send_text):
    if send_text == "登録":
        user_id = user_state.user_id
        user = User.query.filter_by(line_user_id=user_id).first()

        logging.debug(
            f"ユーザ情報を取得しました。lineID→{user.line_user_id},アクセストークン{user.google_access_token}," +
            f"リフレッシュトークン{user.google_refresh_token}")

        credentials = google_auth.get_google_credentials_from_db(user)
        logging.debug(f"認証情報を取得しました")

        if not credentials:
            logging.debug("ここに入ったということは認証情報の取得に失敗している？")
            # 認証リンクを生成してユーザに送信
            auth_link = google_auth.generate_auth_url(user_id)  # トークンを含む認証リンク
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text="下のリンクからGoogle認証を行ってください。\n" + auth_link))
            return

        # 登録する情報を定義
        summary = temp_event.title
        start_time = temp_event.start_time
        end_time = temp_event.end_time
        description = ""
        location = ""
        # ここでGoogleカレンダーに予定の登録をする
        event_link = google_auth.add_event_to_google_calendar(credentials,
                                                              start_time, end_time, summary, description, location)
        logging.debug(f"Googlecalendarへの登録が完了しました")
        # 登録ができたらGooglecalendarのURLを返信する
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="✅予定を追加しました! " + event_link),
                                                       massege.first_quick_reply()])
        logging.debug(f"リンクを返信しました")

        db.session.delete(temp_event)
        db.session.commit()

        # user_stateをクリア
        UserState.user_state_clear(user_state)

    elif send_text == "詳細を続けて入力":

        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(f"詳細の入力に進みます📅 次の指示に従ってください。"),
             massege.send_location()]
            )

        user_state.next_question = config.const_location_input_wait
        db.session.add(user_state)
        db.session.commit()

    else:
        line_bot_api.reply_message(event.reply_token, [massege.send_schedule_temp_confirmation(temp_event)])


def handle_location_input(event, line_bot_api, user_state, temp_event, send_text):
    temp_event.location = send_text
    db.session.add(temp_event)
    db.session.commit()

    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(f"場所を「{send_text}」に決定しました！📍"),
            massege.send_detail()
        ]
    )

    user_state.next_question = config.const_detail_input_wait
    db.session.add(user_state)
    db.session.commit()


def handle_detail_input(event, line_bot_api, user_state, temp_event, send_text):
    temp_event.note = send_text
    db.session.commit()

    line_bot_api.reply_message(event.reply_token, [massege.send_schedule_confirmation(temp_event)])

    user_state.next_question = config.const_confirmation_wait
    db.session.add(user_state)
    db.session.commit()


def handle_confirmation(event, line_bot_api, user_state, temp_event, send_text):
    if send_text == "登録":
        # (中略)
        # (中略) ユーザからの入力を解析して、start_time, end_time, summary などを取得
        user_id = user_state.user_id
        user = User.query.filter_by(line_user_id=user_id).first()

        logging.debug(
            f"ユーザ情報を取得しました。lineID→{user.line_user_id},アクセストークン{user.google_access_token}," +
            f"リフレッシュトークン{user.google_refresh_token}")

        credentials = google_auth.get_google_credentials_from_db(user)
        logging.debug(f"認証情報を取得しました")

        if not credentials:
            logging.debug("ここに入ったということは認証情報の取得に失敗している？")
            # 認証リンクを生成してユーザに送信
            auth_link = google_auth.generate_auth_url(user_id)  # トークンを含む認証リンク
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text="下のリンクからGoogle認証を行ってください。\n" + auth_link))
            return

        # 登録する情報を定義
        summary = temp_event.title
        start_time = temp_event.start_time
        end_time = temp_event.end_time
        description = temp_event.note
        location = temp_event.location

        # ここでGoogleカレンダーに予定の登録をする
        event_link = google_auth.add_event_to_google_calendar(credentials,
                                                              start_time, end_time, summary, description, location)
        logging.debug(f"Googlecalendarへの登録が完了しました")
        # 登録ができたらGooglecalendarのURLを返信する
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="✅予定を追加しました! " + event_link),
                                                       massege.first_quick_reply()])
        logging.debug(f"リンクを返信しました")

        db.session.delete(temp_event)
        db.session.commit()

        # user_stateをクリア
        UserState.user_state_clear(user_state)
        # ここでのGoogleカレンダーへの登録ロジックは、既存のコードをそのまま使用しています。
    else:
        line_bot_api.reply_message(event.reply_token, [massege.send_schedule_confirmation(temp_event)])
