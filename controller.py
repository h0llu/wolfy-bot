import requests

from bs4 import BeautifulSoup

import exceptions
from dbworker import Statistics, Commands, Users


stats = Statistics()
commands = Commands()
users = Users()

# ///////////////////////////////////////////////////////////////////////////
# USERS

def set_user_state(user_id: int, user_state: int, direction: str) -> None:
    users.set_state(user_id, user_state, direction)

def update_user_state(user_id: int, user_state: int) -> None:
    users.update_state(user_id, user_state)

def get_user_state(user_id: int) -> int:
    return users.get_state(user_id)

def get_user_direction(user_id: int) -> str:
    return users.get_direction(user_id)

def set_user_action(user_id: int, action: str) -> None:
    users.set_action(user_id, action)

def get_user_action(user_id: int) -> str:
    return users.get_action(user_id)

# ///////////////////////////////////////////////////////////////////////////
# COMMANDS

def drop_commands() -> None:
    commands.drop()

def get_singles() -> list:
    return commands.get_singles()

def get_directed() -> list:
    return commands.get_directed()

def set_command(user_id: int, command: str) -> None:
    action = users.get_action(user_id)
    direction = users.get_direction(user_id)
    commands.add(action, command, direction)

def del_command(command: str) -> None:
    commands.remove(command)

def play_single(host: str, command: str) -> str:
    action = commands.get_action(command)
    if action == '':
        raise exceptions.NoSuchCommand('Команда не существует!')

    stats.add_single(host, action)
    return f'{host} {action}'

def play_direct(host: str, command: str, target: str) -> str:
    action = commands.get_action(command)
    if action == '':
        raise exceptions.NoSuchCommand('Команда не существует!')

    stats.add_direct(host, action, target)
    return f'{host} {action} @{target}'

# ///////////////////////////////////////////////////////////////////////////
# STATS

def get_all_direct_stats() -> list:
    return stats.get_all_direct()

def get_all_single_stats() -> list:
    return stats.get_all_single()

def get_user_direct_stats(host: str) -> list:
    return stats.get_direct_for_user(host)

def get_user_single_stats(host: str) -> list:
    return stats.get_single_for_user(host)

# ///////////////////////////////////////////////////////////////////////////

def _is_user(username: str) -> bool:
    if username[0] != '@':
        return False
    page = requests.get(f'https://t.me/{username[1:]}')
    soup = BeautifulSoup(page.text, 'html.parser')

    return soup.find('title', text=f'Telegram: Contact {username}') is not None