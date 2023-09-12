from datetime import datetime, timedelta
from linebot.models import (TextSendMessage, CarouselColumn, CarouselTemplate, MessageAction, TemplateSendMessage,
                            QuickReplyButton, QuickReply, MessageEvent, PostbackAction, PostbackEvent)
from models import db, Event, UserState, User, TempEvent, TempDate
import massege
import valid
import logging

logging.basicConfig(level=logging.DEBUG)


class EventHandler:
    def __init__(self, event, line_bot_api):
        self.event = event
        self.user_id = event.source.user_id
        self.line_bot_api = line_bot_api
        self.text_return = "最初に戻る"
        self.text_cansel = "キャンセル"

        # イベントタイプに基づいて属性を設定
        if isinstance(event, MessageEvent):
            self.text = event.message.text
        elif isinstance(event, PostbackEvent):

            pass

    def handle(self):
        # User の取得または作成
        user = self.get_or_create_user()

        # TempEvent の取得または作成
        temp_event = self.get_or_create_temp_event()
        temp_date = self.get_create_temp_date()

        user_state = self.get_or_create_user_state()

        if self.text == '最初に戻る' or self.text == "キャンセル":
            self.handle_cancel(temp_event, user_state)

        elif self.text == '予定の追加':
            user_state.next_question = 'title'
            db.session.add(user_state)
            db.session.commit()
            items = [
                QuickReplyButton(action=MessageAction(label=self.text_return, text=self.text_return)),
            ]

            # クイックリプライの設定
            quick_reply = QuickReply(items=items)
            self.line_bot_api.reply_message(
                self.event.reply_token,
                [TextSendMessage(text=massege.add_message(user_state.next_question, temp_event, self.text_return),
                                 emojis=[
                                     {
                                         "index": 16,
                                         "productId": "5ac21a18040ab15980c9b43e",
                                         "emojiId": "014"
                                     },
                                 ],
                                 quick_reply=quick_reply
                                 )]
            )
            user_state.next_question = 'title_answer'
            db.session.add(user_state)
            db.session.commit()

        elif self.text == '予定の確認':

            user_state.next_question = 'select_confirmation_date'
            db.session.commit()

            self.line_bot_api.reply_message(
                self.event.reply_token,
                [massege.confirmation_sc_message(user_state.next_question)]
            )

        else:
            # --------------------追加フロー-------------------------------------
            if user_state.next_question == 'title_answer':
                self.send_add_title_answer(temp_event, user_state)

            elif user_state.next_question == 'start_time':
                self.send_add_start_time(temp_event, user_state)

            elif user_state.next_question == 'end_time':
                self.send_add_end_time(temp_event, user_state)

            elif user_state.next_question == 'location':
                self.send_add_location(temp_event, user_state)

            elif user_state.next_question == 'note':
                self.send_add_note(temp_event, user_state)

            elif user_state.next_question == 'confirmation':

                if self.text == '登録':
                    # 最後に、すべての情報が入力されたら正式なテーブルに移動
                    if (temp_event.title and temp_event.start_time and temp_event.end_time and temp_event.location
                            and temp_event.note):
                        new_event = Event(
                            user_id=temp_event.user_id,
                            title=temp_event.title,
                            start_time=temp_event.start_time,
                            end_time=temp_event.end_time,
                            location=temp_event.location,
                            note=temp_event.note
                        )
                        db.session.add(new_event)
                        db.session.delete(temp_event)  # 一時的なエントリを削除
                        db.session.commit()

                        # 確認メッセージを送信
                        self.line_bot_api.reply_message(
                            self.event.reply_token,
                            [massege.completion_registration()]
                        )
                        user_state.next_question = 'default'
                        db.session.add(user)
                        db.session.commit()
                    else:

                        self.send_add_note(temp_event, user_state)

            # ---------------------------参照フロー-----------------------------------------------
            elif user_state.next_question == 'select_confirmation_date':
                # 「今日」「明日」「明後日」で選択されるのでそこの予定を一覧表示
                if self.show_events_by_date(self.text):
                    user_state.next_question = "default"
                    db.session.commit()

            else:
                logging.debug("初期メッセージを送信しようとしています。")
                self.handle_default()

    # --------------------------------------基本メソッド---------------------------------------------
    # メッセージ受信時にメッセージを送るユーザがまだdbに存在していない場合、userテーブルとuser_stateテーブルに追加
    def get_or_create_user(self):
        user = User.query.filter_by(line_user_id=self.user_id).first()
        if not user:
            user = User(line_user_id=self.user_id)
            db.session.add(user)
            db.session.commit()
        return user

    # ユーザの状態を取得
    def get_or_create_temp_event(self):
        temp_event = TempEvent.query.filter_by(user_id=self.user_id).first()
        if not temp_event:
            temp_event = TempEvent(user_id=self.user_id)
            db.session.add(temp_event)
            db.session.commit()
        return temp_event

    def get_create_temp_date(self):
        temp_date = TempDate.query.filter_by(user_id=self.user_id).first()
        if not temp_date:
            temp_date = TempEvent(user_id=self.user_id)
            db.session.add(temp_date)
            db.session.commit()
        return temp_date


    def get_or_create_user_state(self):
        user_state = UserState.query.filter_by(user_id=self.user_id).first()
        if not user_state:
            user_state = UserState(user_id=self.user_id)
            db.session.add(user_state)
            db.session.commit()
        return user_state

    def handle_cancel(self, temp_event, user_state):
        user_state.next_question = 'default'
        db.session.delete(temp_event)  # 一時的なエントリを削除
        db.session.commit()
        self.line_bot_api.reply_message(
            self.event.reply_token,
            massege.cancel_message())  # 最初の選択肢を再度表示

    def handle_default(self):
        self.line_bot_api.reply_message(
            self.event.reply_token,
            [massege.first_message()]
        )

    # ---------------------------------------追加フロー---------------------------------------------------------------
    def send_add_title_answer(self, temp_event, user_state):
        temp_event.title = self.text
        db.session.commit()

        user_state.next_question = 'start_time'
        db.session.add(user_state)
        db.session.commit()
        items = [
            QuickReplyButton(action=MessageAction(label=self.text_return, text=self.text_return)),
        ]

        # クイックリプライの設定
        quick_reply = QuickReply(items=items)

        self.line_bot_api.reply_message(
            self.event.reply_token,
            [TextSendMessage(massege.add_message(user_state.next_question, temp_event, self.text_return),
                             quick_reply=quick_reply)]
        )

    def send_add_start_time(self, temp_event, user_state):
        if not (valid.is_valid_date(self.text, '%Y%m%d%H%M')):
            items = [
                QuickReplyButton(action=MessageAction(label=self.text_return, text=self.text_return)),
            ]

            # クイックリプライの設定
            quick_reply = QuickReply(items=items)
            self.line_bot_api.reply_message(
                self.event.reply_token,
                [TextSendMessage(massege.add_message(user_state.next_question, temp_event, self.text_cansel) +
                                 "※※※正しい形式で入力してください※※※\n\n" + "最初に戻る場合は↓を押す",
                                 quick_reply=quick_reply)]
            )

        else:
            temp_event.start_time = datetime.strptime(self.text, '%Y%m%d%H%M')
            db.session.commit()

            user_state.next_question = 'end_time'
            db.session.add(user_state)
            db.session.commit()

            items = [
                QuickReplyButton(action=MessageAction(label=self.text_return, text=self.text_return)),
            ]

            # クイックリプライの設定
            quick_reply = QuickReply(items=items)
            self.line_bot_api.reply_message(
                self.event.reply_token,
                [TextSendMessage(text=massege.add_message(user_state.next_question, temp_event, self.text_cansel),
                                 quick_reply=quick_reply)]
            )

    def send_add_end_time(self, temp_event, user_state):
        if not (valid.is_valid_date(self.text, '%Y%m%d%H%M')):
            items = [
                QuickReplyButton(action=MessageAction(label=self.text_return, text=self.text_return)),
            ]

            # クイックリプライの設定
            quick_reply = QuickReply(items=items)
            self.line_bot_api.reply_message(
                self.event.reply_token,
                [TextSendMessage(text=massege.add_message(user_state.next_question, temp_event, self.text_cansel) +
                                      "\n※※※ただしい形式で再度入力してください※※※\n" + "最初に戻る場合は↓を押す",
                                 quick_reply=quick_reply)]
            )
        else:
            temp_event.end_time = datetime.strptime(self.text, '%Y%m%d%H%M')
            db.session.commit()
            user_state.next_question = 'location'
            db.session.add(user_state)
            db.session.commit()
            items = [
                QuickReplyButton(action=MessageAction(label=self.text_return, text=self.text_return)),
            ]

            # クイックリプライの設定
            quick_reply = QuickReply(items=items)
            self.line_bot_api.reply_message(
                self.event.reply_token,
                [TextSendMessage(text=massege.add_message(user_state.next_question, temp_event, self.text_return),
                                 quick_reply=quick_reply)]
            )

    def send_add_location(self, temp_event, user_state):
        temp_event.location = self.text
        db.session.commit()
        user_state.next_question = 'note'
        db.session.add(user_state)
        db.session.commit()
        items = [
            QuickReplyButton(action=MessageAction(label=self.text_return, text=self.text_return)),
        ]

        # クイックリプライの設定
        quick_reply = QuickReply(items=items)
        self.line_bot_api.reply_message(
            self.event.reply_token,
            [TextSendMessage(text=massege.add_message(user_state.next_question, temp_event, self.text_cansel),
                             quick_reply=quick_reply)]
        )

    def send_add_note(self, temp_event, user_state):
        temp_event.note = self.text
        db.session.commit()
        user_state.next_question = 'confirmation'
        db.session.add(user_state)
        db.session.commit()
        self.line_bot_api.reply_message(
            self.event.reply_token,
            [TextSendMessage(
                text=massege.add_message(user_state.next_question, temp_event, self.text_cansel),
                quick_reply=massege.confirmation_message()
            )]
        )

    # -------------------------参照フロー--------------------------------------------------------------------------------

    def show_events_by_date(self, send_text, page=0):
        """
        指定された日のイベントをカルーセルメッセージとして表示します。

        Parameters:
        - month_selected (str): ユーザーが選択した日 (例: "1" は1日を意味します)

        Returns:
        None: LINE APIを使用してメッセージを送信します
        """

        if not valid.is_valid_date(send_text, "%Y-%m-%d"):
            self.line_bot_api.reply_message(
                self.event.reply_token,
                [massege.confirmation_sc_message("select_confirmation_date")]
            )
            return False

        # 指定された日の開始日時と終了日時を取得
        start_date = datetime.strptime(send_text, "%Y-%m-%d")
        end_date = start_date + timedelta(days=1)

        # 上記の日付範囲内のイベントをデータベースから取得
        # 上記の日付範囲内のイベントをデータベースから取得
        events = Event.query.filter(
            Event.start_time >= start_date,
            Event.start_time < end_date,
            Event.user_id == self.user_id  # ユーザIDでの絞り込みを追加
        ).order_by(Event.start_time).all()

        # イベントが一つも見つからなかった場合の処理
        if not events:
            self.line_bot_api.reply_message(
                self.event.reply_token,
                [massege.month_more_message()]
            )
            return False  # これ以降の処理をスキップするためのreturn

        # イベントをページング
        per_page = 9  # 最後の1つは「次のページ」ボタン用
        start_index = page * per_page
        end_index = start_index + per_page
        paged_events = events[start_index:end_index]

        # イベントをカルーセルメッセージのカラムに変換
        columns = []
        for event in paged_events:
            text = (f"{event.start_time.strftime('%Y-%m-%d %H:%M')} ~ \n" +
                    f"場所: {event.location}\n"
                    + f"メモ: {event.note}")
            if len(text) > 60:
                text = text[:57] + "..."

            column = CarouselColumn(
                title=event.title,
                text=text,
                actions=[
                    PostbackAction(label="詳細を見る", data=f"event_details: {event.id}")
                ]
            )
            columns.append(column)

        # 最後のカラムに「次のページ」ボタンを追加
        if len(events) > end_index:  # さらに表示するイベントがある場合
            next_page_button = CarouselColumn(
                title="More Events...",
                text="Tap to view more events",
                actions=[
                    PostbackAction(label="次のページ", data=f"show_events:{send_text}:{page + 1}")
                ]
            )
            columns.append(next_page_button)

        # カルーセルテンプレートを作成
        carousel_template = CarouselTemplate(columns=columns)

        # クイックリプライのアイテム設定
        confirm_items = [
            QuickReplyButton(action=MessageAction(label="最初に戻る", text="最初に戻る"))
        ]

        # クイックリプライの設定
        quick_reply = QuickReply(items=confirm_items)

        # カルーセルメッセージを作成
        carousel_message = TemplateSendMessage(
            alt_text="イベント一覧",
            template=carousel_template,
            quick_reply=quick_reply
        )

        # LINE APIを使用してカルーセルメッセージを送信
        self.line_bot_api.reply_message(
            self.event.reply_token,
            [carousel_message]
        )

    def handle_next_page_request(self, command):
        # コマンドは "show_events:date:page" の形式と仮定
        _, date_selected, page = command.split(":")
        self.show_events_by_date(date_selected, int(page))

    def get_event_details(self, command):  # データベースからイベントの詳細を取得する関数
        # データベースから指定されたIDのイベントを取得
        action, event_id = command.split(":")
        event = Event.query.filter_by(id=event_id).first()

        if event:
            self.line_bot_api.reply_message(
                self.event.reply_token,
                [massege.get_event_details_message(event)]
            )
        else:
            items = [QuickReplyButton(action=MessageAction(label=self.text_return, text=self.text_return)),]
            quick_reply = QuickReply(items=items)

            self.line_bot_api.reply_message(
                self.event.reply_token,
                [TextSendMessage(text="この予定は現在存在していません。他の予定を選択してください",quick_reply=quick_reply)])

    def delete_schedule(self, command):  # データベースから指定したイベントを削除
        try:
            action, event_id = command.split(":")
            # データベースからイベントを取得
            event_to_delete = Event.query.get(event_id)

            if event_to_delete:
                # イベントをデータベースから削除
                db.session.delete(event_to_delete)
                db.session.commit()

                # 削除成功のメッセージを送信
                items = [
                    QuickReplyButton(action=MessageAction(label="予定の追加", text="予定の追加")),
                    QuickReplyButton(action=MessageAction(label="予定の確認", text="予定の確認"))
                ]

                # クイックリプライの設定
                quick_reply = QuickReply(items=items)

                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    [TextSendMessage(text="イベントを正常に削除しました。\n次は何をお手伝いしましょうか。",
                                     quick_reply=quick_reply)]
                )
            else:
                # イベントが存在しない場合のメッセージを送信
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    TextSendMessage(text="指定されたイベントは存在しません。")
                )

        except Exception as e:
            # エラーが発生した場合のメッセージを送信
            print(f"Error occurred: {e}")
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text="イベントの削除中にエラーが発生しました。")
            )
