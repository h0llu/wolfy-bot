import telebot
from telebot.types import InlineKeyboardButton

def stats():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Полная статистика', callback_data='all'),
               InlineKeyboardButton('Статистика по юзеру', callback_data='users'),
               InlineKeyboardButton('❌ Закрыть', callback_data='close'))
    return markup

def all_stats(directed, singles):
    directed = sorted(directed, key=lambda tup: tup[0])
    singles = sorted(singles, key=lambda tup: tup[0])
    result = '*Полная статистика*\n'
    result += '  *Направленные действия*\n'
    for d in directed:
        result += f'    {d[0]} {d[1]} {d[2]} {d[3]} раз\n'

    result += '  *Ненаправленные действия*\n'
    for s in singles:
        result += f'    {s[0]} {s[1]}  {s[2]} раз\n'

    return result

def all_users():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Гена', callback_data='user_stats h0llu'),
        InlineKeyboardButton('Ксюша', callback_data='user_stats zdesbilaksenia'),
        InlineKeyboardButton('Ваня', callback_data='user_stats ivankot13'),
        InlineKeyboardButton('Артём', callback_data='user_stats I_am_arti'),
        InlineKeyboardButton('Вика', callback_data='user_stats v_pozdn'),
        InlineKeyboardButton('❌ Закрыть', callback_data='close'))

    
    return markup

def user_stats(host, directed, singles):
    directed = sorted(directed, key=lambda tup: tup[1])
    singles = sorted(singles, key=lambda tup: tup[1])
    result = f'*Статистика по {host}*\n'
    result += ' *Направленные действия*\n'
    for d in directed:
        result += f'  {d[0]} {d[1]} {d[2]} {d[3]} раз\n'

    result += ' *Ненаправленные действия*\n'
    for s in singles:
        result += f'  {s[0]} {s[1]}  {s[2]} раз\n'

    return result

def rp():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Ненправленная', callback_data='rp single'),
               InlineKeyboardButton('Направленная', callback_data='rp direct'),
               InlineKeyboardButton('❌ Закрыть', callback_data='close'))
    return markup

def rp_direct(directed):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    directed = sorted(directed, key=lambda tup: tup[0])
    for d in directed:
        markup.add(InlineKeyboardButton(f'{d[1]}\n', callback_data=f'rp_target {d[1]}'))

    markup.add(InlineKeyboardButton('❌ Закрыть', callback_data='close'))
    return markup

def rp_single(singles):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    singles = sorted(singles, key=lambda tup: tup[0])
    for s in singles:
        markup.add(InlineKeyboardButton(f'{s[1]}\n', callback_data=f'rp_single {s[1]}'))

    markup.add(InlineKeyboardButton('❌ Закрыть', callback_data='close'))
    return markup

def rp_target(command: str):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Гена', callback_data=f'rp_direct h0llu {command}'),
        InlineKeyboardButton('Ксюша', callback_data=f'rp_direct zdesbilaksenia {command}'),
        InlineKeyboardButton('Ваня', callback_data=f'rp_direct ivankot13 {command}'),
        InlineKeyboardButton('Артём', callback_data=f'rp_direct I_am_arti {command}'),
        InlineKeyboardButton('Вика', callback_data=f'rp_direct v_pozdn {command}'),
        InlineKeyboardButton('Всем', callback_data=f'rp_direct всем {command}'),
        InlineKeyboardButton('Всех', callback_data=f'rp_direct всех {command}'),
        InlineKeyboardButton('Всеми', callback_data=f'rp_direct всеми {command}'),
        InlineKeyboardButton('❌ Закрыть', callback_data='close'))
    
    return markup

def add():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Ненаправленная', callback_data='add single'),
               InlineKeyboardButton('Направленная', callback_data='add direct'),
               InlineKeyboardButton('❌ Закрыть', callback_data='close'))
    return markup

def delete():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Ненаправленная', callback_data='del single'),
               InlineKeyboardButton('Направленная', callback_data='del direct'),
               InlineKeyboardButton('❌ Закрыть', callback_data='close'))
    return markup

def del_command(directed):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for command in directed:
        markup.add(InlineKeyboardButton(command[1], callback_data=f'del_command {command[1]}'))
    markup.add(InlineKeyboardButton('❌ Закрыть', callback_data='close'))
    return markup

