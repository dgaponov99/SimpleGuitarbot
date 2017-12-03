import telebot
import os
from flask import Flask, request
import config

bot = telebot.TeleBot(config.TOKEN)  # Создание бота как объекта

server = Flask(__name__)  # Создание сервера


# Прием сообщений
@server.route('/' + config.TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


# Установка вебхуков
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=config.URL)
    return "!", 200


# Комманда "/start"
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


# Отправка камертона
@bot.message_handler(commands=["tuner"])
def send_tuner(message):
    f = open('res/tuner.ogg', 'rb')
    msg = bot.send_voice(message.chat.id, f, None)
    f.close()
    bot.send_message(message.chat.id, msg.voice.file_id)


# Отправка изображения аккорда
@bot.message_handler(content_types=["text"])
def send_chords(message):
    try:
        image = open('res/chords/' + message.text.upper() + '.jpg', 'rb')
        bot.send_photo(message.chat.id, image, caption=message.text)
        image.close()
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'В нашей базе нет такого аккорда')


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))  # Запуск сервера
