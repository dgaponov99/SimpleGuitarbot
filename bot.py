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


@server.route('/' + config.TOKEN, methods=['POST'])
def get_message():
    """Прием сообщений"""
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    """Установка вебхуков"""
    bot.remove_webhook()
    bot.set_webhook(url=config.URL)
    return "!", 200


@bot.message_handler(commands=['start'])
def send_start(message):
    """Команда /start"""
    bot.send_message(message.chat.id,
                     string_values.hello + message.from_user.first_name + '!' +
                     '\n' + string_values.description, parse_mode='HTML')


@bot.message_handler(commands=['help'])
def send_help(message):
    """Команда /help"""
    bot.send_message(message.chat.id, string_values.help_description, parse_mode='HTML')


@bot.message_handler(commands=['tutorials'])
def send_tutorial(message):
    """Команда /tutorials"""
    bot.send_message(message.chat.id, string_values.tutorial, parse_mode='HTML')


@bot.message_handler(commands=['tuning_uku'])
def send_tuning_uku(message):
    """Команда /tuning_uku"""
    bot.send_message(message.chat.id, string_values.tuning_ukulele, parse_mode='HTML')


@bot.message_handler(commands=['parts'])
def send_parts(message):
    """Команда /parts"""
    bot.send_photo(message.chat.id, files_id.parts_of_guitar)


@bot.message_handler(commands=['tuning'])
def send_tuning(message):
    """Команда /tuning"""
    bot.send_message(message.chat.id, string_values.tuning, parse_mode='HTML')


@bot.message_handler(commands=["tuner"])
def send_tuner(message):
    """Отправка камертона"""
    bot.send_voice(message.chat.id, files_id.tuner_id, caption=string_values.cpt_tuner)


@bot.message_handler(commands=['care'])
def send_care(message):
    """Команда /care"""
    bot.send_message(message.chat.id, string_values.care, parse_mode='HTML')


@bot.message_handler(commands=['experience'])
def send_experience(message):
    """Команда /experience"""
    bot.send_message(message.chat.id, string_values.experience, parse_mode='HTML')


@bot.message_handler(content_types=["text"])
def send_chords(message):
    """Отправка изображения аккорда"""
    if len(message.text) < 10:
        cap, chord_files_id = chords_db.get_files_id(message.text.lower())
        if chord_files_id is None:
            bot.send_message(message.chat.id, string_values.update)
            chord = parser.Images_chord(message.text)
            caption, chord_urls = chord.get_Url()
            if len(caption) > 0:
                ids = []
                # for chord_url in chord_urls:
                #     img = requests.get(chord_url)
                #     file = bot.send_photo(message.chat.id, img.content, caption=caption)
                #     ids.append(file.photo[0].file_id)
                images = []
                for chord_url in chord_urls:
                    images.append(types.InputMediaPhoto(chord_url))
                messages_file = bot.send_media_group(message.chat.id, images)
                for message_file in messages_file:
                    ids.append(message_file.photo[0].file_id)
                chords_db.set_files_id(message.text.lower(), ids, caption)
                bot.send_message(message.chat.id, string_values.update_complete)
            else:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text=string_values.to_offer,
                                                        callback_data='^$' + str(
                                                            message.from_user.first_name) + '$' + str(
                                                            message.chat.id) + '$' + str(message.text)))
                bot.send_message(message.chat.id, string_values.text_inline_button, reply_markup=keyboard)
        else:
            for chord_file_id in chord_files_id:
                bot.send_photo(message.chat.id, chord_file_id, caption=cap)
    else:
        bot.send_message(message.chat.id, string_values.not_exist)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    """Отправка администраторам заявки на рассмотрение аккорда"""
    a = c.data.split('$')
    if a[0] == '^':
        for admin in config.ADMINS:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(text=string_values.agree,
                                           callback_data='+$' + str(c.message.chat.id) + '$' + str(
                                               c.from_user.first_name)),
                types.InlineKeyboardButton(text=string_values.disagree,
                                           callback_data='-$' + str(c.message.chat.id) + '$' + str(
                                               c.from_user.first_name)),
                types.InlineKeyboardButton(text=string_values.done,
                                           callback_data='*$' + str(c.message.chat.id) + '$' + str(
                                               c.from_user.first_name)))
            bot.send_message(admin, string_values.message_to_admins.format(a[1], a[2], a[3]), reply_markup=keyboard)
    elif a[0] == '+':
        bot.send_message(a[1], string_values.message_to_users_agree)
        for admin in config.ADMINS:
            bot.send_message(admin, a[2] + string_values.message_to_admins_agree)
    elif a[0] == '-':
        bot.send_message(a[1], string_values.message_to_users_disagree)
        for admin in config.ADMINS:
            bot.send_message(admin, a[2] + string_values.message_to_admins_disagree)
    elif a[0] == '*':
        bot.send_message(a[1], string_values.message_to_users_done)
        for admin in config.ADMINS:
            bot.send_message(admin, a[2] + string_values.message_to_admins_done)


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))  # Запуск сервера
