from apscheduler.schedulers.background import BackgroundScheduler
from linebot.models import TextSendMessage

from linebot import LineBotApi

import config

# 他の必要なインポート

#line_bot_api = LineBotApi(config.LINE_ACCESS_TOKEN)


#def check_and_send_reminders():
    #line_bot_api.push_message("Ueb445922680f1104d9de589fc5e45566", TextSendMessage(text="堤です"))


#scheduler = BackgroundScheduler()
#scheduler.add_job(check_and_send_reminders, 'interval', minutes=1)
#scheduler.start()
