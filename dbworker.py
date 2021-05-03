import sqlite3


class Statistics:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('bot.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

        stmt = '''CREATE TABLE IF NOT EXISTS statistics
        (host TEXT NOT NULL,
        action TEXT NOT NULL,
        target TEXT NOT NULL,
        times INTEGER NOT NULL,
        UNIQUE(host, action, target))'''

        self.cursor.execute(stmt)
        self.conn.commit()

    def add(self, host: str, action: str, target: str) -> None:
        stmt = 'INSERT OR IGNORE INTO statistics VALUES (?,?,?,?)'
        args = (host, action, target, 0)
        self.cursor.execute(stmt, args)

        stmt = '''UPDATE statistics SET times = times + 1
        WHERE host = (?) AND
        action = (?) AND
        target = (?)'''
        args = (host, action, target)
        self.cursor.execute(stmt, args)

        self.conn.commit()

    def get_host(self, host: str) -> tuple:
        stmt = 'SELECT * FROM statistics WHERE host = (?)'
        args = (host,)
        self.cursor.execute(stmt, args)

        result = self.cursor.fetchall()
        return result if result is not None else ()

    def get_all(self) -> tuple:
        stmt = 'SELECT * FROM statistics'
        self.cursor.execute(stmt)

        result = self.cursor.fetchall()
        return result if result is not None else ()


class Commands:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('bot.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        stmt = '''CREATE TABLE IF NOT EXISTS actions
        (action text,
        command text primary key)'''
        self.cursor.execute(stmt)
        self.conn.commit()

        self.add('дал смачного леща', 'дать леща')

    def add(self, action: str, command: str) -> None:
        stmt = '''INSERT OR IGNORE INTO actions
        VALUES (?,?)'''
        args = (action, command)
        self.cursor.execute(stmt, args)

        self.conn.commit()

    def get_action(self, command: str) -> tuple:
        stmt = 'SELECT action FROM actions WHERE command = (?)'
        args = (command,)
        self.cursor.execute(stmt, args)

        result = self.cursor.fetchone()
        return result if result is not None else ()

    def get_all(self) -> tuple:
        stmt = 'SELECT * FROM actions'
        self.cursor.execute(stmt)

        result = self.cursor.fetchall()
        return result if result is not None else ()

    def remove(self, command: str) -> None:
        stmt = 'DELETE FROM actions WHERE command = (?)'
        args = (command,)
        self.cursor.execute(stmt, args)

        self.conn.commit()

