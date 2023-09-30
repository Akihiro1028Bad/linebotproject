# 標準ライブラリ
import logging
import json  # <- この行を追加

import config
import secrets
from datetime import datetime, timedelta

# 外部ライブラリ
from flask import url_for, request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from linebot import LineBotApi
from linebot.models import TextSendMessage
import requests

# ローカルモジュール
import massege
from models import User, AuthToken2, db


def generate_auth_url(token):
    """
    Googleの認証ページへのリダイレクトURLを生成する関数。
    実際にリダイレクトするのではなく、URLのみを返します。

    Args:
        token (str): ユーザーセッションを識別するためのトークン。

    Returns:
        str: Googleの認証ページへのリダイレクトURL。
        None: エラーが発生した場合。
    """
    # OAuth2.0のスコープを定義
    scopes = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'openid'
    ]

    credentials_json = config.GOOGLE_CREDENTIALS

    # JSON文字列をPythonの辞書オブジェクトに変換
    credentials_data = json.loads(credentials_json)

    # OAuth2.0のフローを初期化
    flow = InstalledAppFlow.from_client_config(
        credentials_data, scopes=scopes)

    # リダイレクト先のURLを設定 (開発環境に合わせてコメントアウトを切り替え)
    flow.redirect_uri = config.REDIRECT_URI

    try:
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent',
            state=token  # トークンをstateパラメータとして埋め込み
        )
        return authorization_url
    except Exception as e:
        logging.error(f"Error generating the auth URL: {e}")
        return None


def oauth2callback(line_bot_api: LineBotApi):
    """
    Googleの認証完了後に呼ばれるコールバック関数。
    取得したトークンを使用してユーザ情報を取得し、データベースに保存する。
    """
    try:
        # Google認証の結果を取得
        state, flow, service = fetch_google_authentication_result()

        # Googleユーザ情報を取得
        userinfo = service.userinfo().get().execute()
        handle_user_information(userinfo, flow.credentials, state, line_bot_api)

    except ValueError as ve:
        logging.error(f"ValueError occurred: {ve}")
        return "Invalid request parameters."
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return "Googleの認証に失敗しました。再試行してください。"

    return "Googleカレンダー認証成功!! lineのトーク画面にお戻りください。"


def fetch_google_authentication_result():
    """Googleの認証結果を取得する"""
    state = request.args.get('state', None)
    if not state:
        raise ValueError("State parameter is missing in the request.")

    credentials_json = config.GOOGLE_CREDENTIALS

    # JSON文字列をPythonの辞書オブジェクトに変換
    credentials_data = json.loads(credentials_json)

    flow = InstalledAppFlow.from_client_config(
        credentials_data,
        scopes=[
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'openid'
        ]
    )

    flow.redirect_uri = url_for('oauth2callback', _external=True, _scheme='https')
    authorization_response = request.url.replace("http://", "https://")
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    service = build('oauth2', 'v2', credentials=credentials)

    return state, flow, service


def handle_user_information(userinfo, credentials, state, line_bot_api):
    """取得したユーザ情報を処理する"""
    user_email = userinfo.get('email')
    user_id = userinfo.get('id')

    user = User.query.filter_by(google_email=user_email).first()
    token_entry = AuthToken2.query.filter_by(token=state).first()

    if not user:
        if token_entry:
            line_id = token_entry.line_id
        else:
            raise ValueError("Google認証時に一時的に保存されているlineIDが見つかりませんでした")

        User.add_new_user(
            line_user_id=line_id,
            google_user_id=user_id,
            google_email=user_email,
            google_access_token=credentials.token,
            google_refresh_token=credentials.refresh_token,
            token_expiry=credentials.expiry
        )

    # 一時的に保存しているトークンとIDを削除
    AuthToken2.delete_token_data(state)

    # 指定ユーザにlineメッセージを送信
    line_bot_api.push_message(
        to=token_entry.line_id,
        messages=massege.google_certification_success()
    )


def handle_follow(event, line_bot_api: LineBotApi):
    """
    友達追加時のイベント処理。Google認証のリンクを生成してユーザーに返信する。

    :param event: 友達追加時のイベント
    :param line_bot_api: LineのAPI
    :return: None
    """
    try:
        # ランダムなトークンを生成してDBに保存
        token = generate_and_save_token(event.source.user_id)

        # Google認証のURLを生成
        auth_url = generate_auth_url(token)

        # 外部ブラウザを開く用のリンクの作成
        auth_url_new = f"{auth_url}&openExternalBrowser=1"

        # 認証の案内メッセージをユーザーに送信
        send_auth_instruction(event, line_bot_api, massege.message_auth_instruction(auth_url_new))

    except Exception as e:
        logging.error(f"Error occurred during the follow event handling: {e}")


def generate_and_save_token(user_id: str) -> str:
    """
    ランダムなトークンを生成してDBに保存する。

    :param user_id: ユーザID
    :return: 生成したトークン
    """
    token = secrets.token_urlsafe(16)
    AuthToken2.add_token(user_id, token)
    return token


def send_auth_instruction(event, line_bot_api: LineBotApi, TemperMessage_Auth):
    """
    Google認証の案内メッセージをユーザーに送信する。

    :param TemperMessage_Auth: 認証URLのテンプレートメッセージ（ボタン）
    :param event: Lineイベント
    :param line_bot_api: LineのAPI
    :return: None
    """
    intro_message = (
        "はじめまして！スケジュールお兄さんです！⏰\n"
        "このアカウントを活用するためには、Google認証が必要です！✨\n"
        "Google認証を完了すると、Googleカレンダーの予定追加や予定確認など、便利な機能を使用いただけます。\n\n"
        "認証は簡単！\n\n"
        "以下のリンクの手順に従ってください🔗↓↓↓↓\n"
        f"{config.INSTA_PROCESS_URL}\n\n"
        "ご不明な点があれば、お気軽にご連絡くださいね😊"
    )
    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=intro_message), TemperMessage_Auth]
    )


def refresh_access_token(user: User):
    """
    ユーザーのリフレッシュトークンを使用して新しいアクセストークンを取得し、
    それを用いて新しいCredentialsオブジェクトを生成して返す。

    Args:
        user: ユーザー情報（データベースから取得したオブジェクト）

    Returns:
        credentials (oauth2client.client.Credentials): 新しいアクセストークン情報
    """
    token_endpoint = "https://oauth2.googleapis.com/token"

    # トークン更新のためのパラメータを設定
    payload = {
        'client_id': config.GOOGLE_CLIENT_ID,  # configから読み込む
        'client_secret': config.GOOGLE_CLIENT_SECRET,  # configから読み込む
        'refresh_token': user.google_refresh_token,
        'grant_type': 'refresh_token'
    }

    response_data = requests.post(token_endpoint, data=payload).json()

    new_access_token = response_data['access_token']
    expiry_datetime = datetime.utcnow() + timedelta(seconds=response_data['expires_in'])

    # データベースのユーザー情報を更新
    update_user_credentials_in_db(user, new_access_token, expiry_datetime)

    return create_new_credentials(new_access_token, user, expiry_datetime)


def update_user_credentials_in_db(user, new_access_token, expiry_datetime):
    """データベースに保存されているユーザーの認証情報を更新する"""
    user.google_access_token = new_access_token
    user.token_expiry = expiry_datetime
    db.session.add(user)
    db.session.commit()


def create_new_credentials(access_token, user, expiry_datetime):
    """新しいCredentialsオブジェクトを生成して返す"""
    return Credentials(
        token=access_token,
        refresh_token=user.google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=config.GOOGLE_CLIENT_ID,
        client_secret=config.GOOGLE_CLIENT_SECRET,
        scopes=[
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'openid'
        ],
        expiry=expiry_datetime
    )


def add_event_to_google_calendar(credentials, start_time, end_time, summary, description=None, location=None):
    """
    Googleカレンダーに新しいイベントを追加する。

    Args:
        credentials: Google APIへのアクセスのための認証情報
        start_time: イベントの開始時間 (datetimeオブジェクトまたはISOフォーマットの文字列)
        end_time: イベントの終了時間 (datetimeオブジェクトまたはISOフォーマットの文字列)
        summary: イベントの概要
        description: イベントの詳細な説明 (デフォルトはNone)
        location: イベントの場所 (デフォルトはNone)

    Returns:
        str: 追加されたイベントのURL
    """
    # Google カレンダーAPIへの接続を初期化
    service = build('calendar', 'v3', credentials=credentials)

    # datetimeオブジェクトをISOフォーマットに変換
    start_time = format_time_to_iso(start_time)
    end_time = format_time_to_iso(end_time)

    # イベント情報を定義
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Tokyo',
        },
    }

    logging.debug(f"イベント情報: {event}")

    # 定義したイベント情報をGoogleカレンダーに追加
    event = service.events().insert(calendarId='primary', body=event).execute()

    logging.debug("イベントの追加が完了しました。")

    return event.get('htmlLink')


def format_time_to_iso(time):
    """
    datetimeオブジェクトが渡された場合、それをISOフォーマットに変換する。
    すでに文字列の場合はそのまま返す。
    """
    if isinstance(time, datetime):
        return time.isoformat()
    return time


def get_google_credentials_from_db(user):
    """
    指定されたuserに関連付けられているGoogleのアクセストークンをデータベースから取得する。

    Args:
        user: ユーザ情報のオブジェクト

    Returns:
        Credentials: Googleのアクセストークン情報。該当するユーザーがいないか、トークンが存在しない場合はNone。
    """
    user_data = User.query.filter_by(line_user_id=user.line_user_id).first()

    # ユーザ情報がデータベースに存在しない場合
    if not user_data:
        return None

    # アクセストークンの有効期限を確認
    if is_token_expired(user_data):
        # 期限切れの場合、新しいアクセストークンを取得
        credentials = refresh_access_token(user_data)
    else:
        # 有効なアクセストークンが存在する場合、Credentialsオブジェクトを作成
        credentials = create_credentials_from_user(user_data)

    return credentials


def is_token_expired(user_data):
    """トークンの有効期限が切れているか確認する関数"""
    now = datetime.utcnow()
    return not user_data.token_expiry or user_data.token_expiry <= now


def create_credentials_from_user(user_data):
    """ユーザデータからCredentialsオブジェクトを作成する関数"""
    return Credentials(
        token=user_data.google_access_token,
        refresh_token=user_data.google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=config.GOOGLE_CLIENT_ID,  # あなたのクライアントID
        client_secret=config.GOOGLE_CLIENT_SECRET,  # あなたのクライアントシークレット
        scopes=['https://www.googleapis.com/auth/calendar',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
                'openid'],
        expiry=user_data.token_expiry
    )




