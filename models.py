from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import UniqueConstraint, ForeignKeyConstraint
from datetime import datetime


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

    events = db.relationship('Event', backref='user', lazy=True)  # Eventテーブルとのリレーション（必要であれば）

    __table_args__ = (
        UniqueConstraint('google_user_id', name='uq_google_user_id'),
        UniqueConstraint('google_email', name='uq_google_email'),
        UniqueConstraint('line_user_id', name='uq_line_email_google_email'),
    )

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
    - next_question (str): ユーザーに次に提示すべき質問やアクションの情報。
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    next_question = db.Column(db.String(50), nullable=True)


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
    def update_or_insert_line_id(cls, new_line_id):
        """
        LINEユーザーのIDをデータベースにアップデートまたはインサートする。

        引数:
        - new_line_id (str): 保存または更新したいLINEユーザーのID

        戻り値:
        なし
        """
        # 既存のレコードをデータベースから検索
        existing_record = cls.query.first()

        if existing_record:
            # レコードが存在する場合、line_idを新しいものに更新
            existing_record.line_id = new_line_id
            existing_record.created_at = datetime.utcnow()
        else:
            # レコードが存在しない場合、新しいレコードを作成
            new_record = cls(line_id=new_line_id)
            db.session.add(new_record)

        # 上記の変更をデータベースに保存
        db.session.commit()

