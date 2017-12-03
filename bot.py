import os

import telebot
from flask import Flask, request

import config
from res import string_values
from res import files_id

bot = telebot.TeleBot(config.TOKEN)  # Создание объекта бота

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
def send_start(message):
    bot.send_message(message.chat.id,
                     string_values.hello + message.from_user.first_name + '!' +
                     '\n' + string_values.description)


# Комманда "/help"
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, string_values.help_description)


# Отправка камертона
@bot.message_handler(commands=["tuner"])
def send_tuner(message):
    bot.send_voice(message.chat.id, files_id.tuner_id, caption=string_values.cpt_tuner)


# Отправка изображения аккорда
@bot.message_handler(content_types=["text"])
def send_chords(message):
    try:
        # Попытка открытия и отправки картинки
        image = open('res/chords/' + message.text.upper() + '.jpg', 'rb')
        bot.send_photo(message.chat.id, image, caption=message.text)
        image.close()
    except FileNotFoundError:
        # Если такой картинки нет говорим об этом
        bot.send_message(message.chat.id, string_values.not_found_chord)


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))  # Запуск сервера
