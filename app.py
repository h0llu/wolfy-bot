import os
import logging

from flask import Flask, request
import telebot

import roleplay


token = '1795637738:AAH2wALYPU0q0d8fUS1murbWNnkJejc3uLM'
bot = telebot.TeleBot(token)


def auth(func):
    def wrapper(msg):
        if msg.chat.id != -1001356393461:
            bot.send_message(msg.chat.id, 'Access Denied')
            msg.text = ''
        return func(msg)

    return wrapper


@bot.message_handler(commands=['rp'])
@auth
def rp(msg):
    if msg.text == '':
        return
    username = msg.from_user.username
    chat_id = msg.chat.id
    try:
        raw_msg = msg.text[msg.text.find(' ')+1:]
        t = roleplay.get_rp(f'@{username}', raw_msg)
    except Exception as e:
        bot.send_message(chat_id, str(e))
        return
    bot.send_message(chat_id, f'@{username} {t[0]} {t[1]}')

@bot.message_handler(commands=['all'])
@auth
def all(msg):
    if msg.text == '':
        return

    l = roleplay.get_all()
    s = '*Список всех команд*\n'
    for t in l:
        s += f'Действие: {t[0]}, Команда: {t[1]}\n'
    bot.send_message(msg.chat.id, s, parse_mode='Markdown')    


@bot.message_handler(commands=['add'])
@auth
def add(msg):
    if msg.text == '':
        return
    
    chat_id = msg.chat.id
    try:
        raw_msg = msg.text[msg.text.find(' ')+1:]
        roleplay.add_command(raw_msg)
    except Exception as e:
        bot.send_message(chat_id, str(e))
        return
    bot.send_message(chat_id, 'Команда успешно добавлена')

@bot.message_handler(commands=['del'])
@auth
def rem(msg):
    if msg.text == '':
        return

    raw_msg = msg.text[msg.text.find(' ')+1:]
    roleplay.remove_command(raw_msg)

@bot.message_handler(commands=['stats'])
@auth
def stats(msg):
    if msg.text == '':
        return

    chat_id = msg.chat.id

    if msg.text.find(' ') == -1:
        l = roleplay.get_all_stats()
        s = '*Полная статистика*\n'
        for t in l:
            s += f'{t[0]} {t[1]} {t[2]} {t[3]} раз\n'
        bot.send_message(chat_id, s, parse_mode='Markdown')
    else:
        l = roleplay.get_stats(msg.text[msg.text.find(' ')+1:])
        s = f"*Статистика по {msg.text[msg.text.find(' ')+1:]}*\n"
        for t in l:
            s += f'{t[0]} {t[1]} {t[2]} {t[3]} раз\n'
        bot.send_message(chat_id, s, parse_mode='Markdown')


if 'HEROKU' in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route('/bot', methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
        return '!', 200
    @server.route('/')
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url='https://murmuring-savannah-80214.herokuapp.com/bot')
        return '?', 200
    server.run(host='0.0.0.0', port=os.environ.get('PORT', 80))
else:
    bot.remove_webhook()
    bot.polling()
