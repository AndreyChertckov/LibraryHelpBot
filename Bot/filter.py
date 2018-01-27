from telegram.ext import BaseFilter
from books import users


class BooleanFilter(BaseFilter):
    def __init__(self, var):
        self.var = var

    def filter(self, message):
        return self.var


class WordFilter(BaseFilter):
    def __init__(self, word):
        self.word = word

    def filter(self, message):
        return self.word == message.text


class UserFilter(BaseFilter):
    def __init__(self, user_type):
        self.user_type = user_type

    def filter(self, message):
        if self.user_type == "u" and not (message.chat_id in list(users.keys())):
            return True
        elif self.user_type == "p" and users[message.chat_id][0] == 0:
            return True
        elif self.user_type == "l" and users[message.chat_id][0] == 1:
            return True
        else:
            return False
