import sqlite3


class Statistics:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('bot.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

        stmt = '''CREATE TABLE IF NOT EXISTS direct_stats
        (host TEXT NOT NULL,
        action TEXT NOT NULL,
        target TEXT NOT NULL,
        times INTEGER NOT NULL,
        UNIQUE(host, action, target))'''
        self.cursor.execute(stmt)

        stmt = '''CREATE TABLE IF NOT EXISTS single_stats
        (host TEXT NOT NULL,
        action TEXT NOT NULL,
        times INTEGER NOT NULL,
        UNIQUE(host, action))'''
        self.cursor.execute(stmt)

        self.conn.commit()

    def add_single(self, host: str, action: str) -> None:
        stmt = 'INSERT OR IGNORE INTO single_stats VALUES (?,?,?)'
        args = (host, action, 0)
        self.cursor.execute(stmt, args)

        stmt = '''UPDATE single_stats SET times = times + 1
        WHERE host = (?) AND
        action = (?)'''
        args = (host, action)
        self.cursor.execute(stmt, args)

        self.conn.commit()

    def add_direct(self, host: str, action: str, target: str) -> None:
        stmt = 'INSERT OR IGNORE INTO direct_stats VALUES (?,?,?,?)'
        args = (host, action, target, 0)
        self.cursor.execute(stmt, args)

        stmt = '''UPDATE direct_stats SET times = times + 1
        WHERE host = (?) AND
        action = (?) AND
        target = (?)'''
        args = (host, action, target)
        self.cursor.execute(stmt, args)

        self.conn.commit()

    def get_direct_for_user(self, host: str) -> list:
        stmt = 'SELECT * FROM direct_stats WHERE host = (?)'
        args = (host,)
        self.cursor.execute(stmt, args)

        result = self.cursor.fetchall()
        return result if result is not None else []

    def get_single_for_user(self, host: str) -> list:
        stmt = 'SELECT * FROM single_stats WHERE host = (?)'
        args = (host,)
        self.cursor.execute(stmt, args)

        result = self.cursor.fetchall()
        return result if result is not None else []

    def get_all_direct(self) -> list:
        stmt = 'SELECT * FROM direct_stats'
        self.cursor.execute(stmt)
        result = self.cursor.fetchall()

        return result if result is not None else []

    def get_all_single(self) -> list:
        stmt = 'SELECT * FROM single_stats'
        self.cursor.execute(stmt)
        result = self.cursor.fetchall()
        
        return result if result is not None else []


class Commands:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('bot.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        stmt = '''CREATE TABLE IF NOT EXISTS actions
        (action text,
        command text primary key,
        direction text)'''
        self.cursor.execute(stmt)
        self.conn.commit()

    def drop(self) -> None:
        stmt = 'DELETE FROM actions'
        self.cursor.execute(stmt)
        self.conn.commit()

    def add(self, action: str, command: str, direction: str) -> None:
        stmt = '''INSERT OR IGNORE INTO actions
        VALUES (?,?,?)'''
        args = (action, command, direction)
        self.cursor.execute(stmt, args)
        self.conn.commit()

    def get_action(self, command: str) -> str:
        stmt = 'SELECT action FROM actions WHERE command = (?)'
        args = (command,)
        self.cursor.execute(stmt, args)

        result = self.cursor.fetchone()
        return result[0] if result is not None else ''

    def get_singles(self) -> list:
        stmt = 'SELECT * FROM actions WHERE direction = (?)'
        args = ('single',)
        self.cursor.execute(stmt, args)

        result = self.cursor.fetchall()
        return result if result is not None else []

    def get_directed(self) -> list:
        stmt = 'SELECT * FROM actions WHERE direction = (?)'
        args = ('direct',)
        self.cursor.execute(stmt, args)

        result = self.cursor.fetchall()
        return result if result is not None else []

    def get_all(self) -> list:
        stmt = 'SELECT * FROM actions'
        self.cursor.execute(stmt)

        result = self.cursor.fetchall()
        return result if result is not None else []

    def remove(self, command: str) -> None:
        stmt = 'DELETE FROM actions WHERE command = (?)'
        args = (command,)
        self.cursor.execute(stmt, args)

        self.conn.commit()


class Users:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('bot.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        stmt = '''CREATE TABLE IF NOT EXISTS users
        (user_id integer primary key,
         user_state integer,
         direction text,
         action text)'''
        self.cursor.execute(stmt)
        self.conn.commit()

    def set_state(self, user_id: int, user_state: int, direction: str) -> None:
        stmt = 'INSERT OR REPLACE INTO users VALUES (?,?,?,?)'
        args = (user_id, user_state, direction, '')
        self.cursor.execute(stmt, args)
        self.conn.commit()

    def update_state(self, user_id: int, user_state: int) -> None:
        stmt = '''UPDATE OR IGNORE users SET user_state = (?)
        WHERE user_id = (?)'''
        args = (user_state, user_id)
        self.cursor.execute(stmt, args)
        self.conn.commit()

    def get_state(self, user_id: int) -> int:
        stmt = 'SELECT user_state FROM users WHERE user_id = (?)'
        args = (user_id,)
        self.cursor.execute(stmt, args)

        result = self.cursor.fetchone()
        return result[0] if result is not None else -1

    def get_direction(self, user_id: int) -> str:
        stmt = 'SELECT direction FROM users WHERE user_id = (?)'
        args = (user_id,)
        self.cursor.execute(stmt, args)

        result = self.cursor.fetchone()
        return result[0] if result is not None else ''

    def set_action(self, user_id: int, action: str) -> None:
        stmt = '''UPDATE users SET action = (?)
        WHERE user_id = (?)'''
        args = (action, user_id)
        self.cursor.execute(stmt, args)
        self.conn.commit()

    def get_action(self, user_id: int) -> str:
        stmt = 'SELECT action FROM users WHERE user_id = (?)'
        args = (user_id,)
        self.cursor.execute(stmt, args)

        result = self.cursor.fetchone()
        return result[0] if result is not None else ''