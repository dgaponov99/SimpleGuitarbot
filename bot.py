import telebot
import os
from flask import Flask, request

import Config

bot = telebot.TeleBot(Config.TOKEN)

server = Flask(__name__)
server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))


@server.route('/' + Config.TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=Config.URL)
    return "!", 200


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


