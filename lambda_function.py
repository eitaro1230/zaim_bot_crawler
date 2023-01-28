from datetime import datetime, timedelta

from config import config
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage
from zaim_crawler.original_pyzaim import ZaimCrawler
from zaim_crawler.zaim_crawler import ZaimBotMessageCreate


def lambda_handler(event, context):
    # 毎月1日は先月の1日~31日分の情報を集計する
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    ten_days_ago = today - timedelta(days=10)
    last_month_last_day = today.replace(day=1) - timedelta(days=1)
    last_month_first_day = last_month_last_day.replace(day=1)

    (first_day, last_day) = (
        (last_month_first_day, last_month_last_day)
        if today.day == today.replace(day=1).day
        else (ten_days_ago, yesterday)
    )

    # ZaimCrawlerをインスタンス化
    crawler = ZaimCrawler(
        selenium_path=config.SELENIUM_PATH,
        driver_path=config.CHROME_DRIVER_PATH,
        docker_selenium_ipaddress=None,
    )

    crawler.login(
        user_id=config.ZAIM_USER_ID,
        password=config.ZAIM_PASSWORD,
    )

    # zaimからデータを集計する
    data = crawler.get_data(str(last_day.year), str(last_day.month))
    if any(data):
        zaim_bot_message = ZaimBotMessageCreate()
        zaim_bot_message_text: str = zaim_bot_message.zaim_bot_message_text(
            zaim_crawler_list=data,
            type="payment",
            first_day=first_day,
            last_day=last_day,
        )
    else:
        zaim_bot_message_text = "対象期間のデータがありませんでした。"

    try:
        # LineBotApiをインスタンス化
        line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
        # lineに送付する
        line_bot_api.push_message(
            to=config.LINE_MESSAGE_TO_ID,
            messages=TextSendMessage(text=zaim_bot_message_text),
        )
    except LineBotApiError as e:
        # error handle
        error_message = {
            "status_code": f"{e.status_code}",
            "message": e.message,
        }
        print(error_message)
