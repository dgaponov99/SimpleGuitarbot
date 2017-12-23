import os

import requests
import telebot
from flask import Flask, request
from telebot import types

import config
from res import string_values
from res import files_id
from spliter import split_array_of_ten
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
                chord_urls = split_array_of_ten(chord_urls)
                for url_box in chord_urls:
                    if len(url_box) > 1:
                        images = []
                        for chord_url in url_box:
                            images.append(types.InputMediaPhoto(chord_url))
                        try:
                            messages_file = bot.send_media_group(message.chat.id, images)
                        except Exception:
                            messages_file = []
                            bot.send_message(message.chat.id, string_values.message_exception)
                            for admin in config.ADMINS:
                                bot.send_message(admin, string_values.message_exception_loading_media_to_admin)
                        for message_file in messages_file:
                            ids.append(message_file.photo[0].file_id)
                    else:
                        img = requests.get(url_box[0])
                        file = bot.send_photo(message.chat.id, img.content)
                        ids.append(file.photo[0].file_id)
                if len(ids) > 0:
                    chords_db.set_files_id(message.text.lower(), ids, caption)
            else:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text=string_values.to_offer,
                                                        callback_data='^$' + str(
                                                            message.from_user.first_name) + '$' + str(
                                                            message.chat.id) + '$' + str(message.text)))
                bot.send_message(message.chat.id, string_values.text_inline_button, reply_markup=keyboard)
        else:
            chord_files_id = split_array_of_ten(chord_files_id)
            for chord_files_box in chord_files_id:
                if len(chord_files_box) > 1:
                    images = []
                    for chord_file_id in chord_files_box:
                        images.append(types.InputMediaPhoto(chord_file_id))
                    bot.send_media_group(message.chat.id, images)
                else:
                    bot.send_photo(message.chat.id, chord_files_box[0])
    else:
        bot.send_message(message.chat.id, string_values.not_exist)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    """Отправка администраторам заявки на рассмотрение аккорда"""
    a = c.data.split('$')
    if a[0] == '^':
        # Создание вариантов ответа у администраторов
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
        # Уведомление о добавлении аккорда
        bot.send_message(a[1], string_values.message_to_users_agree)
        for admin in config.ADMINS:
            bot.send_message(admin, str(c.from_user.first_name) + string_values.message_to_admins_agree)
    elif a[0] == '-':
        # Уведомление об отклонении заявки
        bot.send_message(a[1], string_values.message_to_users_disagree)
        for admin in config.ADMINS:
            bot.send_message(admin, str(c.from_user.first_name) + string_values.message_to_admins_disagree)
    elif a[0] == '*':
        # Уведомление об обработки заявки
        bot.send_message(a[1], string_values.message_to_users_done)
        for admin in config.ADMINS:
            bot.send_message(admin, str(c.from_user.first_name) + string_values.message_to_admins_done)


server.run(host="0.0.0.0", port=80)
server = Flask(__name__)
