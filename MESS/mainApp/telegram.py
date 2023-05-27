import requests
import os
import dotenv
from django.conf import settings

dotenv_file = os.path.join(settings.BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.read_dotenv(dotenv_file)

token = os.environ['telegram_token']  # Replace with your Telegram Bot API token
chat_id = os.environ['telegram_chat_id']  # Replace with the chat ID where you want to send the message
timeout_seconds = 2  # Replace with your desired timeout value in seconds



def send_msg_to_telegram(message):

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id,'text': message}

    response = requests.post(url, data=data, timeout=timeout_seconds)




def send_file_to_telegram(chat_id,file_path):
    url = f'https://api.telegram.org/bot{token}/sendDocument'

    files = {'document': open(file_path, 'rb')}
    data = {'chat_id': chat_id}

    response = requests.post(url, files=files, data=data)

    return response.status_code

