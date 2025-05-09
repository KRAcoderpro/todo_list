import requests

from django.conf import settings


def send_telegram_message(chat_id, message):
	print(settings.TELEGRAM_BOT_TOKEN)
	url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
	payload = {
		"chat_id": chat_id,
		"text": message
	}

	response = requests.post(url, data=payload)

	if response.status_code != 200:
		raise Exception(f"Failed to send message: {response.text}")
