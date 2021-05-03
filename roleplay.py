import requests
from bs4 import BeautifulSoup

import exceptions
from dbworker import Commands, Statistics


commands = Commands()
stats = Statistics()


def get_rp(host: str, raw_message: str) -> tuple:
    if len(raw_message) == 0 or raw_message.find(' ') == -1:
        raise exceptions.IncorrectInput(
            'Некорректный ввод'
        )

    command = raw_message[:raw_message.rfind(' ')]
    target = raw_message[raw_message.rfind(' ')+1:]
    
    if not _is_user(target) and \
        target != 'всех' and \
            target != 'всем':
        raise exceptions.NoSuchUser(
            f'Пользователь {target} не существует'
        )

    action = commands.get_action(command)
    if action == ():
        raise exceptions.NoSuchCommand(
            'Команда не существует'
        )
        
    action = action[0]
    if target[0] == '@':
        target = target[1:]

    stats.add(host[1:], action, target)
    return (action, target)

def remove_command(command: str) -> None:
    commands.remove(command)

def get_all() -> list:
    return commands.get_all()

def add_command(raw_message: str) -> None:
    if len(raw_message) == 0 or raw_message.find(',') == -1:
        raise exceptions.IncorrectInput(
            'Некорректный ввод'
        )

    action = raw_message[:raw_message.find(',')]
    command = raw_message[raw_message.find(',')+2:]

    commands.add(action, command)

def get_stats(host: str) -> tuple:
    return stats.get_host(host)

def get_all_stats() -> list:
    return stats.get_all()

def _is_user(username: str) -> bool:
    if username[0] != '@':
        return False
    page = requests.get(f'https://t.me/{username[1:]}')
    soup = BeautifulSoup(page.text, 'html.parser')

    return soup.find('title', text=f'Telegram: Contact {username}') is not None






def main():
    '''Добавляем новое действие'''
    action = 'пизданул'
    command = 'ебнуть'
    add_command(f'{action}, {command}')
    add_command(f'{action}, ударить')

    '''Посмотреть список всех действий и команд'''
    print(get_all())

    '''Заюзать действие'''
    raw_message = 'ударить @h0llu'
    print(get_rp('@h0llu', raw_message))

    '''Удалить команду'''
    remove_command(',')
    print(get_all())

    '''Посмотреть статистику'''
    print(get_stats('@h0llu'))
    print(get_all_stats())

if __name__ == '__main__':
    main()