from telegram.ext import BaseFilter
from Controller.controller import Controller


# Filter for boolean operation
class BooleanFilter(BaseFilter):
    def __init__(self, var):
        self.var = var

    def filter(self, message):
        return self.var


# Filter for check location
# class LocationFilter(BaseFilter):
#     def __init__(self, obj, loc):
#         self.obj = obj
#         self.loc = loc
#
#     def filter(self, message):
#         return self.obj.keyboard_dict[self.loc] == self.obj.keyboardmarkup.keyboard


# Filter for check word
class WordFilter(BaseFilter):
    def __init__(self, word):
        self.word = word

    def filter(self, message):
        return self.word == message.text


# Filter for type of users
class UserFilter(BaseFilter):
    def __init__(self, user_type, invert=False):
        self.user_type = user_type
        self.invert = invert

    def filter(self, message):
        return (self.user_type == Controller().user_type(message.chat_id)) != self.invert


# Filter for check registration of users
class RegFilter(BaseFilter):
    def __init__(self, is_in_reg):
        self.is_in_reg = is_in_reg

    def filter(self, message):
        return message.chat_id in self.is_in_reg
