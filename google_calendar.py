import logging

from flask import request

from flask import jsonify

from googleapiclient.discovery import build

import auth


def create_event(service, start_time_str, end_time_str, summary, description=None, location=None):
    """
    Googleカレンダーに新しいイベントを追加する関数。

    :param service: 認証済みのGoogleカレンダーサービスインスタンス。
    :param start_time_str: イベントの開始時刻（文字列形式、例："2023-01-01T12:00:00"）。
    :param end_time_str: イベントの終了時刻（文字列形式）。
    :param summary: イベントのタイトルや概要。
    :param description: イベントの詳細説明（オプション）。
    :param location: イベントの場所（オプション）。

    :return: 追加されたイベントの情報を含む辞書。
    """

    # イベント情報の辞書を作成
    event_body = {
        'summary': summary,
        'description': description,
        'location': location,
        'start': {
            'dateTime': start_time_str,
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': end_time_str,
            'timeZone': 'Asia/Tokyo',
        },
    }
    try:
        # イベントをGoogleカレンダーに追加
        event = service.events().insert(calendarId='primary', body=event_body).execute()
        # 追加されたイベントの情報を返す
        return event

    except Exception as e:
        logging.error(f"An error occurred while creating the event: {e}")
        return None


def delete_event(service, event_id):
    """
    Googleカレンダーから指定されたIDのイベントを削除する関数。

    :param service: 認証済みのGoogleカレンダーサービスインスタンス。
    :param event_id: 削除するイベントのID。

    :return: イベントの削除に成功した場合はTrue、失敗した場合はFalse。
    """

    try:
        # Googleカレンダーから指定されたIDのイベントを削除
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return True
    except Exception as e:
        # エラーが発生した場合、エラーメッセージを表示
        logging.error(f"An error occurred: {e}")
        return False


def update_event(service, event_id, start_time_str=None, end_time_str=None, summary=None, description=None, location=None):
    try:
        # イベントを取得
        event = service.events().get(calendarId='primary', eventId=event_id).execute()

        # 更新する情報を設定
        if summary:
            event['summary'] = summary
        if description:
            event['description'] = description
        if location:
            event['location'] = location
        if start_time_str:
            event['start']['dateTime'] = start_time_str
        if end_time_str:
            event['end']['dateTime'] = end_time_str

        # イベントを更新
        updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        return updated_event

    except Exception as e:
        logging.error(f"An error occurred while updating the event: {e}")
        return None




