from telegram.ext import BaseFilter
from Controller.controller import Controller


class BooleanFilter(BaseFilter):
    def __init__(self, var):
        self.var = var

    def filter(self, message):
        return self.var


class LocationFilter(BaseFilter):
    def __init__(self, obj, loc):
        self.obj = obj
        self.loc = loc

    def filter(self, message):
        return self.obj.keyboard_dict[self.loc] == self.obj.keyboardmarkup.keyboard


class WordFilter(BaseFilter):
    def __init__(self, word):
        self.word = word

    def filter(self, message):
        return self.word == message.text

class UserFilter(BaseFilter):
    def __init__(self, user_type):
        self.user_type = user_type

    def filter(self, message):
        chat_id = message.chat_id
        ctrl = Controller()
        if self.user_type == "u" and not ctrl.chat_exists(chat_id):
            return True
        elif self.user_type == "p" and (ctrl.get_user(chat_id)["status"] == "Faculty" or ctrl.get_user(chat_id)["status"] == "student"):
            return True
        elif self.user_type == "l" and ctrl.get_user(chat_id)["status"] == "Librarian":
            return True
        else:
            return False