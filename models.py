# 標準ライブラリ
import logging
from datetime import datetime, timedelta, time

# 外部ライブラリ
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import UniqueConstraint

# ローカルモジュール
import config


# SQLAlchemyを初期化
db = SQLAlchemy()


# Userモデル（テーブル）を定義
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    line_user_id = db.Column(db.String(128), unique=True, nullable=False)  # lineのユーザーID
    google_user_id = db.Column(db.String(128), unique=True, nullable=False)  # GoogleのユーザーID
    google_email = db.Column(db.String(255), unique=True, nullable=False)  # Googleのメールアドレス
    google_access_token = db.Column(db.String(255), nullable=True)  # Googleのアクセストークン
    google_refresh_token = db.Column(db.String(255), nullable=True)  # Googleのリフレッシュトークン
    token_expiry = db.Column(db.DateTime, nullable=True)  # トークンの有効期限
    is_notification_enabled = db.Column(db.Boolean, default=True)
    notification_time = db.Column(db.Time, nullable=True, default=time(6, 0))

    events = db.relationship('Event', backref='user', lazy=True)  # Eventテーブルとのリレーション（必要であれば）

    __table_args__ = (
        UniqueConstraint('google_user_id', name='uq_google_user_id'),
        UniqueConstraint('google_email', name='uq_google_email'),
        UniqueConstraint('line_user_id', name='uq_line_email_google_email'),
    )

    @classmethod
    def get_all_user_ids_from_db(cls):
        """
        すべてのLINEユーザーIDをデータベースから取得する。

        Returns:
            list: LINEユーザーIDのリスト
        """
        return [user.line_user_id for user in cls.query.all()]

    @classmethod
    def add_new_user(cls, line_user_id, google_user_id, google_email,
                     google_access_token=None, google_refresh_token=None, token_expiry=None):
        new_user = User(
            line_user_id=line_user_id,
            google_user_id=google_user_id,
            google_email=google_email,
            google_access_token=google_access_token,
            google_refresh_token=google_refresh_token,
            token_expiry=token_expiry
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def user_exists(cls, line_user_id):
        """
        指定したLINEユーザIDのユーザが存在するかどうかを調べる関数

        :param line_user_id: 調べたいLINEユーザID
        :return: ユーザが存在する場合はTrue, しない場合はFalse
        """
        user = User.query.filter_by(line_user_id=line_user_id).first()
        logging.debug("ユーザテーブルにユーザが存在するか調べました")
        return user is not None


# Eventモデル（テーブル）を定義
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外部キー
    title = db.Column(db.String(255), nullable=False)  # イベントのタイトル
    start_time = db.Column(db.DateTime, nullable=False)  # 開始時間
    end_time = db.Column(db.DateTime, nullable=False)  # 終了時間
    location = db.Column(db.String(255), nullable=True)  # 場所
    note = db.Column(db.Text, nullable=True)  # メモ
    reminders = db.relationship('Reminder', backref='event', lazy=True)  # Reminderテーブルとのリレーショ

    @classmethod
    def add_new_event(cls, user_id, title, start_time, end_time, location=None, note=None):
        """
        新しいイベントをデータベースに追加するメソッド

        :param user_id: ユーザーID
        :param title: イベントのタイトル
        :param start_time: イベントの開始時刻（文字列形式、例："2023-01-01 12:00"）
        :param end_time: イベントの終了時刻（文字列形式、例："2023-01-01 13:00"）
        :param location: イベントの場所（オプション）
        :param note: イベントに関するメモ（オプション）
        """

        new_event = cls(
            user_id=user_id,
            title=title,
            start_time=start_time,
            end_time=end_time,
            location=location,
            note=note
        )
        db.session.add(new_event)
        db.session.commit()

        return new_event  # 追加されたイベントオブジェクトを返す

    # イベントテーブルのデータを取得
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            # その他のフィールドもここに
            'user_id': self.user_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'Location': self.location,
            'note': self.note
        }


class TempEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    note = db.Column(db.Text, nullable=True)

    @classmethod
    def add_new_temp_event(cls, user_id, title=None, start_time=None, end_time=None, location=None, note=None):
        """
        新しいユーザーの状態をデータベースに追加するメソッド。

        Parameters:
        - user_id (int): 追加するユーザーのID。
        - next_question (str): ユーザーに次に提示する質問やアクションの情報。
        - operation (str): ユーザーの操作の情報。

        Returns:
        - instance: 作成されたUserStateのインスタンス。
        """
        temp_event = cls(user_id=user_id, title=title, start_time=start_time, end_time=end_time, location=location,
                         note=note)
        db.session.add(temp_event)
        db.session.commit()
        return temp_event

    @classmethod
    def temp_event_clear(cls, temp_event):
        db.session.delete(temp_event)
        db.session.commit()

        logging.debug("Temp_eventを削除しました")


# Reminderモデル（テーブル）を定義
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)  # 外部キー
    reminder_time = db.Column(db.DateTime, nullable=False)  # リマインダー時間
    status = db.Column(db.String(50), nullable=False)  # ステータス（例：発火済み、未発火など）

    @classmethod
    def add_new_reminder(cls, event_id, reminder_time_str, status='未発火'):
        """
        新しいリマインダーをデータベースに追加するメソッド

        :param event_id: イベントID
        :param reminder_time_str: リマインダーの発火時刻（文字列形式、例："2023-01-01 11:50"）
        :param status: リマインダーのステータス（デフォルトは '未発火'）
        """
        reminder_time = datetime.strptime(reminder_time_str, '%Y-%m-%d %H:%M')

        new_reminder = cls(
            event_id=event_id,
            reminder_time=reminder_time,
            status=status
        )
        db.session.add(new_reminder)
        db.session.commit()

        return new_reminder  # 追加されたリマインダーオブジェクトを返す


class UserState(db.Model):
    """
    UserStateテーブルは、各ユーザーの現在の状態や次に取るべきアクションに関する情報を保存するためのテーブルです。
    例えば、ボットとの対話の中でユーザーが次にどの質問に答えるべきか、などの状態の管理に利用されます。

    Attributes:
    - id (int): レコードの一意のID（主キー）。
    - user_id (int): ユーザーテーブルの外部キー。どのユーザーの状態であるかを示します。
    - operation (str):　現在ユーザが行っている操作を保存しています（追加、確認、編集、消去、リマインドなど）
    - next_question (str): ユーザーに次に提示すべき質問やアクションの情報。
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    operation = db.Column(db.String(50), nullable=True)
    next_question = db.Column(db.String(50), nullable=True)

    @classmethod
    def add_new_user(cls, user_id, next_question=None, operation=None):
        """
        新しいユーザーの状態をデータベースに追加するメソッド。

        Parameters:
        - user_id (int): 追加するユーザーのID。
        - next_question (str): ユーザーに次に提示する質問やアクションの情報。
        - operation (str): ユーザーの操作の情報。

        Returns:
        - instance: 作成されたUserStateのインスタンス。
        """
        user_state = cls(user_id=user_id, next_question=next_question, operation=operation)
        db.session.add(user_state)
        db.session.commit()
        return user_state

    @classmethod
    def user_operation_set(cls, user_state, operation):
        """
        user_stateテーブルのoperationカラムの情報を任意の物に設定するメソッド
        :param user_state:user_stateテーブルのインスタンス
        :param operation:任意の操作状況
        :return:
        """
        user_state.operation = operation
        db.session.add(user_state)
        db.session.commit()
        logging.debug(f"user_state.operationを更新しました。オペレーション→{user_state.operation}")

    @classmethod
    def user_next_question_set(cls, user_state, next_question):
        user_state.next_question = next_question
        db.session.add(user_state)
        db.session.commit()
        logging.debug(f"user_state.next_questionを更新しました。ネクストクエスチョン→{user_state.next_question}")

    @classmethod
    def user_state_clear(cls, user_state):
        user_state.next_question = config.const_default
        db.session.add(user_state)
        db.session.commit()

        user_state.operation = config.const_default
        db.session.add(user_state)
        db.session.commit()

        logging.debug("user_stateをクリアしました")
        logging.debug(f"user_state.operationをクリアしました。オペレーション→{user_state.operation}")
        logging.debug(f"user_state.next_questionをクリアしました。ネクストクエスチョン→{user_state.next_question}")


class TempDate(db.Model):
    """
    TempDateテーブルは、ユーザーによって一時的に入力された年、月、日の情報を保存するためのテーブルです。
    このテーブルは、短期的な情報の保存や、一時的なデータのキャッシュに利用されることを想定しています。

    Attributes:
    - id (int): レコードの一意のID（主キー）。
    - user_id (int): ユーザーテーブルの外部キー。
    - year (int): 年の情報。
    - month (int): 月の情報。
    - day (int): 日の情報。
    """
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外部キー
    year = db.Column(db.Integer, nullable=False)  # 年
    month = db.Column(db.Integer, nullable=False)  # 月
    day = db.Column(db.Integer, nullable=False)  # 日


class TempLineID(db.Model):
    # ID カラム: 一意な主キーとして使用
    id = db.Column(db.Integer, primary_key=True)

    # line_id カラム: LINEユーザーのIDを保存。ユニークな値を持つことを保証
    line_id = db.Column(db.String(255), unique=True, nullable=False)

    # created_at カラム: レコードが作成された日時を保存
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def find_or_create_by_line_id(cls, line_id):
        """
        LINEユーザーのIDに基づいてデータベースからレコードを検索し、存在すればそのレコードを返す。
        存在しない場合は新しいレコードを作成して返す。

        引数:
        - line_id (str): 検索または作成したいLINEユーザーのID

        戻り値:
        - record: 検索または作成されたレコード
        """
        # line_idと一致するレコードをデータベースから検索
        record = cls.query.filter_by(line_id=line_id).first()

        if not record:
            # レコードが存在しない場合、新しいレコードを作成
            record = cls(line_id=line_id)
            db.session.add(record)
            db.session.commit()

        # 検索または作成されたレコードを返す
        return record


class AuthToken(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    line_id = db.Column(db.String, unique=True, nullable=False)
    token = db.Column(db.String, unique=True, nullable=False)
    gmail_address = db.Column(db.String, nullable=True)
    expiration_time = db.Column(db.DateTime, nullable=False)  # 有効期限のカラムも追加

    @classmethod
    def add_token(cls, line_id, token):
        # 現在の時間から1時間後の有効期限を計算
        expiration = datetime.utcnow() + timedelta(hours=1)

        # 指定したline_idを持つエントリをデータベースから検索
        existing_entry = AuthToken.query.filter_by(line_id=line_id).first()

        if existing_entry:
            # 既存のエントリが見つかった場合
            logging.info(f"{line_id} のトークンと有効期限を更新します。")

            # トークンと有効期限を更新
            existing_entry.token = token
            existing_entry.expiration_time = expiration
        else:
            # 既存のエントリが見つからなかった場合
            logging.info(f"{line_id} の新しいエントリを追加します。")

            # 新しいレコードを作成してデータベースに追加
            auth_token = AuthToken(line_id=line_id, token=token, expiration_time=expiration)
            db.session.add(auth_token)

        # データベースの変更をコミット
        try:
            db.session.commit()
            logging.info("データベースの変更を正常にコミットしました。")
        except Exception as e:
            logging.error(f"データベースへの変更のコミットに失敗しました。エラー: {e}")

    @classmethod
    def get_line_id_by_token(cls, token):
        auth_token = cls.query(AuthToken).filter_by(token=token).first()
        if auth_token and auth_token.expiration_time > datetime.utcnow():
            return auth_token.line_id
        else:
            return None

    @classmethod
    def delete_token_data(cls, token):
        try:
            # トークンを使用して関連するレコードを検索
            token_entry = cls.query.filter_by(token=token).first()

            # レコードが見つかった場合
            if token_entry:
                # データベースセッションからそのレコードを削除
                db.session.delete(token_entry)

                # 変更内容をデータベースにコミット
                db.session.commit()

                return True
            else:
                logging.warning(f"No data found for token: {token}")
                return False

        except Exception as e:
            logging.error(f"Error deleting token data: {e}")
            return False
