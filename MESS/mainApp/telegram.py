import requests
import os
import dotenv
from django.conf import settings

dotenv_file = os.path.join(settings.BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.read_dotenv(dotenv_file)

token = os.environ['telegram_token']  # Replace with your Telegram Bot API token
chat_id = os.environ['telegram_chat_id']  # Replace with the chat ID where you want to send the message


def send_msg_to_telegram(message):

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id,'text': message}

    response = requests.post(url, data=data)


    if response.status_code == 200:
        print('Message sent successfully.')
    else:
        print('Failed to send message.')
