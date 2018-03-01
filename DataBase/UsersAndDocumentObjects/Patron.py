from DataBase.UsersAndDocumentObjects.user import userBase


# Class representing 'Patron' object
# inherits from class 'UserBase'
# addes new attributes:
# --- history[] - documents which user took in the past
# --- current_books[] - documents which user has now
# --- check_out_time - on how much time user can take materials
class Patron(userBase):
    __metaclass__ = type

    def __init__(self, name, address, id, status, phone, history=None, current_books=None):
        userBase.__init__(self, name, address, id, phone)
        self.status = status
        self.__history = history
        self.__current_books = current_books
        # self.__check_out_time = check_out_time

    def get_history(self):
        return self.__history

    def get_info(self):
        if self.__history:
            return (self.get_id(),
                    self.get_name(),
                    self.get_address(),
                    self.get_phone(),
                    str(self.__history),
                    str(self.__current_books),
                    self.status)
        else:
            return (self.get_id(),
                    self.get_name(),
                    self.get_address(),
                    self.get_phone(),
                    self.status)
