from telegram.ext import BaseFilter
from Controller.controller import Controller


# Filter for boolean operation
class BooleanFilter(BaseFilter):
    def __init__(self, var):
        self.var = var

    def filter(self, message):
        return self.var


# Filter for check location
class LocationFilter(BaseFilter):
    def __init__(self, obj, loc):
        self.obj = obj
        self.loc = loc

    def filter(self, message):
        return self.obj[message.chat_id][0] == self.loc


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


# Filter for checking state of users
class StateFilter(BaseFilter):
    def __init__(self, state_table):
        self.state_table = state_table

    def filter(self, message):
        return message.chat_id in self.state_table


# Filter for cheking location users in system (stert menu, library etc.)
class LocationFilter(BaseFilter):
    # localUser -- dict of location of all users
    # goalLocal -- need location
    def __init__(self, localUser, goalLocal):
        self.userlocal = localUser
        self.goal = goalLocal

    def filter(self, message):
        if message.chat_id in self.userlocal:
            return self.userlocal[message.chat_id] == self.goal
        else:
            return True