import os

import requests
import telebot
from flask import Flask, request

import config
from res import string_values
from res import files_id
import parser

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


# Команда "/start"
@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id,
                     string_values.hello + message.from_user.first_name + '!' +
                     '\n' + string_values.description)


# Команда "/help"
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, string_values.help_description)


# Команда "/tutorial"
@bot.message_handler(commands=['tutorial'])
def send_tutorial(message):
    bot.send_message(message.chat.id, string_values.tutorial)


# Команда "/tuning_uku"
@bot.message_handler(commands=['tuning_uku'])
def send_tuning_uku(message):
    bot.send_message(message.chat.id, string_values.tuning_ukulele)


# Команда "/memes"
# @bot.message_handler(commands=['memes'])
# def send_memes(message):
# bot.send_message(message.chat.id, string_values.memes)


# Команда "/parts"
@bot.message_handler(commands=['parts'])
def send_parts(message):
    image = open('res/tutorial/parts.jpg', 'rb')
    bot.send_photo(message.chat.id, image)
    image.close()


# Команда "/tuning"
@bot.message_handler(commands=['tuning'])
def send_tuning(message):
    bot.send_message(message.chat.id, string_values.tuning)


# Отправка камертона
@bot.message_handler(commands=["tuner"])
def send_tuner(message):
    bot.send_voice(message.chat.id, files_id.tuner_id, caption=string_values.cpt_tuner)


# Отправка изображения аккорда
@bot.message_handler(content_types=["text"])
def send_chords(message):
    chord = parser.Images_chord(message.text)
    caption, chord_urls = chord.getUrl()
    if len(caption) > 0:
        for chord_url in chord_urls:
            img = requests.get(chord_url)
            bot.send_photo(message.chat.id, img.content, caption=caption)
    else:
        bot.send_message(message.chat.id, 'Такого аккорда нет')  # Добавить кнопку предложения


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))  # Запуск сервера
