from telegram.ext import BaseFilter
from Controller.controller import Controller


# Filter for boolean operation
class BooleanFilter(BaseFilter):
    def __init__(self, var):
        self.var = var

    def filter(self, message):
        return self.var


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


# Filter for checking location users in system (main menu, library etc.)
class LocationFilter(BaseFilter):
    # user_locations -- a dictionary containing the locations of all users
    # location -- required location
    def __init__(self, user_locations, location):
        self.user_location = user_locations
        self.location = location

    def filter(self, message):
        if message.chat_id in self.user_location:
            return self.user_location[message.chat_id] == self.location
        else:
            return False
