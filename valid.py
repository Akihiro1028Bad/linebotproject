from datetime import datetime
import logging
logging.basicConfig(level=logging.DEBUG)


def is_valid_date(date_string, format_str):
    """
    指定した文字列が日付型に変換できるかどうかをチェックする関数

    Parameters:
    - date_string (str): チェックする日付の文字列
    - format_str (str): 日付のフォーマット（例: "%Y-%m-%d"）

    Returns:
    bool: 文字列が日付型に変換できる場合はTrue、それ以外の場合はFalse
    """
    try:
        datetime.strptime(date_string, format_str)
        return True
    except ValueError:
        return False


def is_valid_month(date_string, format_str):
    """
    指定した文字列が日付型に変換できるかどうかをチェックする関数

    Parameters:
    - date_string (str): チェックする日付の文字列
    - format_str (str): 日付のフォーマット（例: "%Y-%m-%d"）

    Returns:
    bool: 文字列が日付型に変換できる場合はTrue、それ以外の場合はFalse
    """
    try:
        datetime.strptime(date_string, format_str)
        return True
    except ValueError:
        return False


def is_valid_year(user_response):
    """
    ユーザからの年の選択が有効かどうかを確認する。

    Parameters:
    - user_response (str): ユーザからの年の選択。

    Returns:
    bool: 選択が有効な場合はTrue、それ以外の場合はFalse。
    """
    logging.debug("年の入力チェックに入ってます")
    # 現在の年を取得する
    current_year = datetime.now().year

    # 選択できる年のリストを作成する (例: 現在の年から過去3年分)
    selectable_years = [str(year) for year in range(current_year - 0, current_year + 3)]

    # ユーザの応答が選択可能な年の中にあるか確認する
    if user_response in selectable_years:
        return True  # 正しい選択
    else:
        return False  # 不正な選択



