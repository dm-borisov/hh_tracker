from environs import Env
from datetime import datetime, timedelta
from fake_useragent import UserAgent
from extract import process_data


import requests


url: str = "https://api.hh.ru/vacancies"

text: str = (
    "удаленно NAME:((analyst OR DWH OR ETL OR SQL) "
    "NOT business NOT системный NOT system NOT 1С "
    "NOT financial NOT финансовый NOT SOC NOT экономист)"
)

date_diff: datetime = datetime.now() - timedelta(minutes=10)
date_from: str = date_diff.strftime("%Y-%m-%dT%H:%M")

params: dict = {
    "text": text,
    "date_from": date_from,
    "per_page": 100
}

ua = UserAgent()
headers = {"User-Agent": ua.random}

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
chat_id = env('CHAT_ID')


def send_message_to_chat(bot_token: str, chat_id: str, url: str,
                         params: dict, headers: dict | None = None):
    """
    Send message with vacancies to chat

    Parameters
    ----------
    bot_token: str
        bot token
    chat_id: str
        chat id where to send message
    url: str
        URL of the requested page
    params: dict
        Query parameters
    headers: dict
        Optional headers for the request
    """
    method_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    method_params = {
        "chat_id": chat_id,
        "text": process_data(url, params=params, headers=headers)
    }

    requests.get(method_url, method_params)


send_message_to_chat(bot_token, chat_id, url, params, headers)
