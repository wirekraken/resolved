from flask import Flask, request, jsonify
from flask_sslify import SSLify

import requests
import json


# setWebHooks
#'https://api.telegram.org/bot1090506253:AAEAvpVx2l8_pqTjiR7-CLn_QQdbvu7G9cg/setWebhook?url=https://alexkraken.pythonanywhere.com/'

app = Flask(__name__)
sslify = SSLify(app)

token = '1090506253:AAEAvpVx2l8_pqTjiR7-CLn_QQdbvu7G9cg'

BASE_URI = 'https://api.telegram.org/bot' + token + '/'


path = '/home/AlexKraken/bot/'

def save_JSON(data, filename=path + 'data.json'):
	with open(filename, 'w') as file:
		json.dump(data, file, indent=4)


def send_message(chat_id, text='what do you want from me?'):
	uri = BASE_URI + 'sendMessage'
	answer = {'chat_id' : chat_id, 'text' : text}
	query = requests.post(uri, json=answer)
	return query.json()



buttons = {
    "inline_keyboard": [
        [{
                "text": "Button",
                "callback_data": "asnwer button1"
            }
        ],
        [{
                "text": "Link",
                "callback_data": "answer button2",
                "url": "google.com"
            }, {
                "text": "Redirect contact",
                "switch_inline_query": "other channel"
            }, {
                "text": "Answer channel",
                "switch_inline_query_current_chat": "exactly"
            }
        ]]
}

def send_message_buttons(chat_id, reply_markup, text='don\'t see buttons?'):
	uri = BASE_URI + 'sendMessage'
	answer = {'chat_id' : chat_id, 'text' : text, 'reply_markup' : reply_markup}
	query = requests.post(uri, json=answer)
	return query.json()


@app.route('/info', methods=['POST', 'GET'])
def get_message():
	with open(path + 'data.json', 'r') as file:
		json_data = file.read()
	data = '<pre>' + json_data + '</pre>'

	return data



@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		response = request.get_json()
		chat_id = response['message']['chat']['id']
		message = response['message']['text']

		save_JSON(response)

		if message.lower() == 'hello':
			send_message(chat_id, text='Shalom')
		elif message.lower() == '/buttons':
			send_message_buttons(chat_id, buttons, text='some buttons')
			pass
		else:
			send_message(chat_id)

		return jsonify(response)

	return '<h1 style=\'text-align:center; font-size:60px; color:coral\'>Hey there, I\'m a Telegram bot :)</h1>'


if __name__ == '__main__':
	app.run(debug=True)
