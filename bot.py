import telebot
import os
from flask import Flask, request
import Config

bot = telebot.TeleBot(Config.TOKEN)  # Создание бота как объекта

server = Flask(__name__)  # Создание сервера


# Прием сообщений
@server.route('/' + Config.TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


# Установка вебхуков
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=Config.URL)
    return "!", 200


# Комманда "/start"
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


# Отправка изображения аккорда
@bot.message_handler(content_types=["text"])
def send_chords(message):
    try:
        image = open('res/chords/' + message.text.upper() + '.jpg', 'rb')
        bot.send_photo(message.chat.id, image)
        image.close()
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'В нашей базе нет такого аккорда')


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))  # Запуск сервера
server = Flask(__name__)  # Наверно это нужно, чтобы Heroku не засыпал
