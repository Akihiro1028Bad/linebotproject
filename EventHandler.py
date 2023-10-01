# 標準ライブラリ
import logging
from datetime import datetime

# 外部ライブラリ
from linebot.models import TextSendMessage, TemplateSendMessage, MessageEvent, PostbackEvent

# ローカルモジュール
import config
import google_auth
import massege
import EventAdd
from models import db, UserState, User, TempEvent, TempDate


logging.basicConfig(level=logging.DEBUG)


class EventHandler:
    def __init__(self, event, line_bot_api):
        self.event = event
        self.user_id = event.source.user_id
        self.line_bot_api = line_bot_api

        # イベントタイプに基づいて属性を設定
        if isinstance(event, MessageEvent):
            self.text = event.message.text

        elif isinstance(event, PostbackEvent):
            pass

    def handle(self):
        logging.debug("hendleメソッドに入りました。")

        if not User.user_exists(self.user_id):
            google_auth.handle_follow(self.event, self.line_bot_api)

        # TempEvent の取得または作成
        temp_event = self.get_or_create_temp_event()

        # ユーザの現在の状態を取得or作成
        user_state = self.get_or_create_user_operation_state()
        logging.debug(f"ユーザID→{user_state.user_id}")
        logging.debug(f"operation→{user_state.operation}")
        logging.debug(f"ネクストクエスチョン→{user_state.next_question}")

        # 入力文字列が「最初に戻る」「キャンセルの場合」
        if self.text == config.const_text_cansel or self.text == config.const_text_return:
            # ユーザの状態を初期に戻す。
            self.handle_cancel(temp_event, user_state)

        elif self.text == config.const_operation_add:

            logging.debug("操作の判定を正しく行っています。")
            # 予定追加の操作を書く
            # user_stateとtemp_eventをクリア
            UserState.user_state_clear(user_state)
            # 開始日時の質問メッセージを送信
            self.begin_date_input_wait(user_state)

        elif self.text == config.const_operation_confirmation:
            # 予定確認の操作
            # user_stateとtemp_eventをクリア
            UserState.user_state_clear(user_state)
            TempEvent.temp_event_clear(temp_event)
            # ユーザの操作状態を「予定の確認」に設定
            UserState.user_operation_set(user_state, config.const_operation_confirmation)

            # 最初の予定の範囲を指定してもらうメッセージを送信
            self.line_bot_api.reply_message(self.event.reply_token, massege.range_select_carousel())

        else:
            if user_state.operation == config.const_operation_add:
                if user_state.next_question == config.const_begin_date_input_wait:
                    # 開始日時の質問メッセージを送信
                    self.begin_date_input_wait(user_state)
                elif user_state.next_question == config.const_finish_date_input_wait:
                    # 終了日時の質問メッセージを送信
                    quick_reply = massege.return_quick_reply()

                    # 返信
                    template_message = TemplateSendMessage(
                        alt_text='終了日時を選択してください',
                        template=massege.end_date_picker_template(),
                        quick_reply=quick_reply
                    )

                    messages = [template_message]

                    self.line_bot_api.reply_message(self.event.reply_token,
                                                    messages)
                else:
                    logging.debug("開始日時、終了日時以外の質問を行うメソッドを実行します")
                    EventAdd.event_add_question(self.event, self.line_bot_api, user_state, temp_event)
            else:
                logging.debug("初期メッセージ送信")
                # 初期メッセージを送信
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    [massege.first_quick_reply()]
                )

    # --------------------------------------基本メソッド---------------------------------------------
    # メッセージ受信時にメッセージを送るユーザがまだdbに存在していない場合、userテーブルとuser_stateテーブルに追加
    def get_or_create_user(self):
        user = User.query.filter_by(line_user_id=self.user_id).first()
        if not user:
            # ここに入ることはおそらくない
            # もし入った場合は、Google認証を済ませていないまま登録される
            user = User(line_user_id=self.user_id)
            db.session.add(user)
            db.session.commit()
        return user

    # ユーザの状態を取得
    def get_or_create_temp_event(self):
        logging.debug("get_or_create_temp_eventが呼び出されました")
        temp_event = TempEvent.query.filter_by(user_id=self.user_id).first()
        logging.debug(f"temp_event = {temp_event}")
        if not temp_event:
            temp_event = TempEvent(user_id=self.user_id)
            db.session.add(temp_event)
            db.session.commit()
            logging.debug("temp_eventにデータが追加されました")
        return temp_event

    def get_create_temp_date(self):
        temp_date = TempDate.query.filter_by(user_id=self.user_id).first()
        if not temp_date:
            temp_date = TempEvent(user_id=self.user_id)
            db.session.add(temp_date)
            db.session.commit()
        return temp_date

    # 現在のユーザの質問フローを設定、取得する
    def get_or_create_user_operation_state(self):
        """
        ユーザの操作状態を取得、または新規作成するメソッド。

        1. ユーザの操作状態が存在しない場合、新規に作成する。
        2. 既に存在する場合、その操作状態を取得する。

        Returns:
            user_state (UserState): ユーザの操作状態
        """
        logging.debug("ユーザの操作状態の取得・作成処理を開始します。")

        # ユーザの操作状態が存在するか確認
        user_state = UserState.query.filter_by(user_id=self.user_id).first()

        # 存在しない場合、新規作成
        if not user_state:
            logging.debug("ユーザの操作状態が存在しないため、新規に作成します。")
            user_state = UserState(
                user_id=self.user_id,
                operation=config.const_default,
                next_question=config.const_default
            )
            db.session.add(user_state)
            db.session.commit()

        logging.debug(f"操作状態の取得が完了しました。ネクストクエスチョン: {user_state.next_question}")
        logging.debug(f"操作状態の取得が完了しました。オペレーション: {user_state.operation}")

        return user_state

    def handle_cancel(self, temp_event, user_state):

        # 現在のユーザの状態を初期状態にリセット
        UserState.user_state_clear(user_state)

        self.line_bot_api.reply_message(
            self.event.reply_token,
            massege.first_quick_reply())  # 最初の選択肢を再度表示

    def handle_default(self):
        self.line_bot_api.reply_message(
            self.event.reply_token,
            [massege.first_quick_reply()]
        )

    # ---------------------------------------追加フロー---------------------------------------------------------------
    def finish_date_input(self):
        # 終了日時が選択されたときの処理
        selected_datetime_str = self.event.postback.params["datetime"]
        selected_datetime_obj = datetime.strptime(selected_datetime_str, '%Y-%m-%dT%H:%M')

        temp_event = TempEvent.query.filter_by(user_id=self.user_id).first()
        user_state = self.get_or_create_user_operation_state()

        if (user_state.next_question == config.const_finish_date_input_wait
                and user_state.operation == config.const_operation_add):

            if selected_datetime_obj < temp_event.start_time:
                # 開始日が終了日よりもあとに設定されてしまった場合は、再度終了日の入力を指示する
                formatted_datetime_end = selected_datetime_obj.strftime('%Y年%m月%d日 %H時%M分')
                formatted_datetime_start = temp_event.start_time.strftime('%Y年%m月%d日 %H時%M分')

                quick_reply = massege.return_quick_reply()

                template_message = TemplateSendMessage(
                    alt_text='終了日時を選択してください',
                    template=massege.end_date_picker_template(),
                    quick_reply=quick_reply
                )
                self.line_bot_api.reply_message(self.event.reply_token,
                                                [TextSendMessage(text="⚠️エラー⚠️\n 「終了日」が不正です!\n" 
                                                                    "「終了日」が「開始日」よりも早い日付に設定されています。\n" 
                                                                    "正しい「終了日」を入力してください。📅\n"
                                                                      f"選択された開始日；{formatted_datetime_start}\n"
                                                                      f"選択された終了日：{formatted_datetime_end}")
                                                    , template_message])
            else:
                temp_event.end_time = selected_datetime_obj
                db.session.add(temp_event)

                formatted_datetime = selected_datetime_obj.strftime('%Y年%m月%d日 %H時%M分')
                informed_message = TextSendMessage(text=f"終了日時を{formatted_datetime}に正しく設定しました👍")

                # 返信
                self.line_bot_api.reply_message(self.event.reply_token,
                                                [informed_message, massege.send_title()])

                # ユーザの操作状態を更新
                UserState.user_next_question_set(user_state, config.const_title_input_wait)
                UserState.user_operation_set(user_state, config.const_operation_add)

        else:
            # 指定のステータスの場合以外にこのポストバックが行われた場合は、一時保存のデータを消去し初期の動作へ
            UserState.user_state_clear(user_state)

            self.line_bot_api.reply_message(self.event.reply_token,
                                            [TextSendMessage(text="予期せぬ動作が行われたので、最初からやり直します")
                                                , massege.first_quick_reply()])

    def begin_date_input(self):
        logging.debug("begin_date_inputメソッドに入りました")
        # 開始日時が選択されたときの処理
        selected_datetime_str = self.event.postback.params["datetime"]
        selected_datetime_obj = datetime.strptime(selected_datetime_str, '%Y-%m-%dT%H:%M')

        temp_event = TempEvent.query.filter_by(user_id=self.user_id).first()
        logging.debug(f"temp_eventを取得しました。")
        user_state = self.get_or_create_user_operation_state()
        logging.debug(f"user_stateを取得しました。ネクストクエスチョン→{user_state.next_question}")
        logging.debug(f"user_stateを取得しました。オペレーション→{user_state.operation}")

        if (user_state.next_question == config.const_begin_date_input_wait
                and user_state.operation == config.const_operation_add):
            temp_event.start_time = selected_datetime_obj
            db.session.add(temp_event)
            logging.debug(f"temp_event.start_timeを更新しました。start_time→{selected_datetime_obj}")

            formatted_datetime = selected_datetime_obj.strftime('%Y年%m月%d日 %H時%M分')
            informed_message = TextSendMessage(text=f"開始日時を{formatted_datetime}に設定しました📅"
                                                    f"\n次に、終了日時を教えてください！🕰️")
            quick_reply = massege.return_quick_reply()

            # 返信
            template_message = TemplateSendMessage(
                alt_text='終了日時を選択してください',
                template=massege.end_date_picker_template(),
                quick_reply=quick_reply
            )

            messages = [informed_message, template_message]

            self.line_bot_api.reply_message(self.event.reply_token,
                                            messages)

            # ユーザの操作状態を更新
            # ユーザの操作状態を「予定の追加」に設定
            UserState.user_operation_set(user_state, config.const_operation_add)
            UserState.user_next_question_set(user_state, config.const_finish_date_input_wait)

        else:
            UserState.user_state_clear(user_state)
            logging.debug("user_stateリセットしました")

            self.line_bot_api.reply_message(self.event.reply_token,
                                            [TextSendMessage(text="予期せぬ動作が行われたので、最初からやり直します")
                                                , massege.first_quick_reply()])

    def begin_date_input_wait(self, user_state):
        # 返信
        template_message = TemplateSendMessage(
            alt_text='開始日時を選択してください',
            template=massege.begin_date_picker_template(),
            quick_reply=massege.return_quick_reply()
        )

        # 返信
        self.line_bot_api.reply_message(self.event.reply_token, template_message)
        # ユーザの操作状態を「予定の追加」に設定
        UserState.user_operation_set(user_state, config.const_operation_add)
        UserState.user_next_question_set(user_state, config.const_begin_date_input_wait)