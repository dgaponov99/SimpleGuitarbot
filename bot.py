import os

import requests
import telebot
from flask import Flask, request
from telebot import types

import config
from res import string_values
from res import files_id
import parser
import chords_db

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
                     '\n' + string_values.description, parse_mode='HTML')


# Команда "/help"
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, string_values.help_description, parse_mode='HTML')


# Команда "/tutorial"
@bot.message_handler(commands=['tutorial'])
def send_tutorial(message):
    bot.send_message(message.chat.id, string_values.tutorial, parse_mode='HTML')


# Команда "/tuning_uku"
@bot.message_handler(commands=['tuning_uku'])
def send_tuning_uku(message):
    bot.send_message(message.chat.id, string_values.tuning_ukulele, parse_mode='HTML')


# Команда "/parts"
@bot.message_handler(commands=['parts'])
def send_parts(message):
    image = open('res/tutorial/parts.jpg', 'rb')
    bot.send_photo(message.chat.id, image)
    image.close()


# Команда "/tuning"
@bot.message_handler(commands=['tuning'])
def send_tuning(message):
    bot.send_message(message.chat.id, string_values.tuning, parse_mode='HTML')


# Отправка камертона
@bot.message_handler(commands=["tuner"])
def send_tuner(message):
    bot.send_voice(message.chat.id, files_id.tuner_id, caption=string_values.cpt_tuner)


# Команда "/care"
@bot.message_handler(commands=['care'])
def send_care(message):
    bot.send_message(message.chat.id, string_values.care, parse_mode='HTML')


# Команда "/experience"
@bot.message_handler(commands=['experience'])
def send_experience(message):
    bot.send_message(message.chat.id, string_values.experience, parse_mode='HTML')


# Отправка изображения аккорда
@bot.message_handler(content_types=["text"])
def send_chords(message):
    chord_files_id = chords_db.get_files_id(message.text.lower())
    if chord_files_id is None:
        bot.send_message(message.chat.id, string_values.update)
        chord = parser.Images_chord(message.text)
        caption, chord_urls = chord.getUrl()
        if len(caption) > 0:
            ids = []
            for chord_url in chord_urls:
                img = requests.get(chord_url)
                msg = bot.send_photo(message.chat.id, img.content, None)
                ids.append(msg.photo[0].file_id)
            chords_db.set_files_id(message.text.lower(), ids)
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Предложить', callback_data=message.text))
            bot.send_message(message.chat.id, string_values.text_inline_button, reply_markup=keyboard)
    else:
        for chord_file_id in chord_files_id:
            bot.send_photo(message.chat.id, chord_file_id)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    for admin in ['445372638', '404752400']:
        bot.send_message(chat_id=admin,
                         text='пользователь ' + str(c.message.chat.id) + ' хочет добавить аккорд ' + c.data)


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))  # Запуск сервера
