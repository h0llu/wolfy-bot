import logging
import os
import requests

import telebot
from flask import Flask

import keyboard
import controller


token = '1795637738:AAH2wALYPU0q0d8fUS1murbWNnkJejc3uLM'
bot = telebot.TeleBot(token)


# ///////////////////////////////////////////////////////////////////////////////////////////

def auth(func):
    def wrapper(msg):
        if msg.chat.id != -1001356393461:
            bot.send_message(msg.chat.id, 'Access Denied')
            msg.text = ''
            return
        return func(msg)

    return wrapper

def vanya_auth(func):
    def wrapper(msg):
        if msg.from_user.id == 263714017:
            bot.send_message(msg.chat.id, 'Access Denied')
            msg.text = ''
            return
        return func(msg)

    return wrapper

# ///////////////////////////////////////////////////////////////////////////////////////////

@bot.callback_query_handler(func=lambda call: call.data == 'close')
def close(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)

# ///////////////////////////////////////////////////////////////////////////////////////////

@bot.message_handler(commands=['all'])
@auth
def all(msg):
    if msg.text == '':
        return

    directed = controller.get_directed()
    singles = controller.get_singles()
    
    directed = sorted(directed, key=lambda tup: tup[0])
    singles = sorted(singles, key=lambda tup: tup[0])
    result = '*Список всех действий*\n'
    result += '  *Направленные действия*\n'
    for d in directed:
        result += f'    Действие: {d[0]}\n    Команда: {d[1]}\n\n'
    
    result += '  *Ненаправленные действия*\n'
    for s in singles:
        result += f'    Действие: {s[0]}\n    Команда: {s[1]}\n\n'
    bot.send_message(msg.chat.id, result, parse_mode='Markdown') 

# ///////////////////////////////////////////////////////////////////////////////////////////

@bot.message_handler(commands=['rp'])
@auth
def rp(msg):
    bot.send_message(msg.chat.id, 'Выберите тип команды', reply_markup=keyboard.rp())

@bot.callback_query_handler(func=lambda call: call.data == 'rp single')
def rp_single(call):
    bot.edit_message_text('Выберите команду', call.message.chat.id, call.message.message_id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=keyboard.rp_single(controller.get_singles()))

@bot.callback_query_handler(func=lambda call: call.data == 'rp direct')
def rp_direct(call):
    bot.edit_message_text('Выберите команду', call.message.chat.id, call.message.message_id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=keyboard.rp_direct(controller.get_directed()))

@bot.callback_query_handler(func=lambda call: call.data.split(' ')[0] == 'rp_target')
def rp_target(call):
    bot.edit_message_text('Выберите цель действия',
        call.message.chat.id, call.message.message_id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
        reply_markup=keyboard.rp_target(' '.join(call.data.split(' ')[1:])))

@bot.callback_query_handler(func=lambda call: call.data.split(' ')[0] == 'rp_direct')
def rp_play_direct(call):
    host = call.from_user.username
    target = call.data.split(' ')[1]
    command = ' '.join(call.data.split(' ')[2:])
    try:
        bot.edit_message_text(controller.play_direct(host, command, target),
            call.message.chat.id, call.message.message_id)
    except Exception as e:
        bot.edit_message_text(str(e),
            call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.split(' ')[0] == 'rp_single')
def rp_play_single(call):
    host = call.from_user.username
    command = ' '.join(call.data.split(' ')[1:])
    try:
        bot.edit_message_text(controller.play_single(host, command),
            call.message.chat.id, call.message.message_id)
    except Exception as e:
        bot.edit_message_text(str(e),
            call.message.chat.id, call.message.message_id)

# ///////////////////////////////////////////////////////////////////////////////////////////

@bot.message_handler(commands=['stats'])
@auth
def stats(msg):
    bot.send_message(msg.chat.id, 'Выберите тип статистики', reply_markup=keyboard.stats())

@bot.callback_query_handler(func=lambda call: call.data == 'all')
def all_stats(call):
    directed = controller.get_all_direct_stats()
    singles = controller.get_all_single_stats()
    bot.edit_message_text(keyboard.all_stats(directed, singles),
    call.message.chat.id, call.message.message_id, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'users')
def select_user_for_stats(call):
    bot.edit_message_text('Выберите пользователя',
        call.message.chat.id, call.message.message_id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
        reply_markup=keyboard.all_users())

@bot.callback_query_handler(func=lambda call: call.data.split(' ')[0] == 'user_stats')
def user_stats(call):
    directed = controller.get_user_direct_stats(call.data[11:])
    singles = controller.get_user_single_stats(call.data[11:])
    bot.edit_message_text(keyboard.user_stats(call.data[11:], directed, singles),
    call.message.chat.id, call.message.message_id, parse_mode='Markdown')

# ///////////////////////////////////////////////////////////////////////////////////////////

@bot.message_handler(commands=['add'])
@auth
def add(msg):
    bot.send_message(msg.chat.id, 'Выберите тип новой команды', reply_markup=keyboard.add())

@bot.callback_query_handler(func=lambda call: call.data == 'add single')
def add_single(call):
    controller.set_user_state(call.from_user.id, 1, 'single')
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, 'Введите новое действие:')

@bot.callback_query_handler(func=lambda call: call.data == 'add direct')
def add_direct(call):
    controller.set_user_state(call.from_user.id, 1, 'direct')
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, 'Введите новое действие:')

@bot.message_handler(func=lambda msg:
    controller.get_user_state(msg.from_user.id) == 1)
def set_action(msg):
    controller.set_user_action(msg.from_user.id, msg.text)
    controller.update_user_state(msg.from_user.id, 2)
    bot.send_message(msg.chat.id, 'Введите команду для нового действия:')

@bot.message_handler(func=lambda msg:
    controller.get_user_state(msg.from_user.id) == 2)
def set_command(msg):
    controller.set_command(msg.from_user.id, msg.text)
    controller.update_user_state(msg.from_user.id, 0)
    bot.send_message(msg.chat.id, 'Команда добавлена')

# ///////////////////////////////////////////////////////////////////////////////////////////

@bot.message_handler(commands=['del'])
@auth
def delete(msg):
    bot.send_message(msg.chat.id, 'Выберите тип команды', reply_markup=keyboard.delete())

@bot.callback_query_handler(func=lambda call: call.data == 'del single')
def del_single(call):
    bot.edit_message_text('Выберите команду, которую хотите удалить',
    call.message.chat.id, call.message.message_id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=keyboard.del_command(controller.get_singles()))

@bot.callback_query_handler(func=lambda call: call.data == 'del direct')
def del_direct(call):
    bot.edit_message_text('Выберите команду, которую хотите удалить',
    call.message.chat.id, call.message.message_id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=keyboard.del_command(controller.get_directed()))

@bot.callback_query_handler(func=lambda call: call.data.split(' ')[0] == 'del_command')
def del_command(call):
    controller.del_command(call.data[12:])
    bot.edit_message_text('Команда удалена', call.message.chat.id, call.message.message_id)

# ///////////////////////////////////////////////////////////////////////////////////////////



def main():
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

if __name__ == '__main__':
    main()