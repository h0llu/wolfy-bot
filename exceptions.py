'''Кастомные исключения, генерируемые приложением'''

class NoSuchUser(Exception):
    pass

class NoSuchCommand(Exception):
    pass

class IncorrectInput(Exception):
    pass