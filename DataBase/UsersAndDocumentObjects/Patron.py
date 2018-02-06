from DataBase.UsersAndDocumentObjects.user import userBase


# Class representing 'Patron' object
# inherits from class 'UserBase'
# addes new attributes:
# --- history[] - documents which user took in the past
# --- current_books[] - documents which user has now
# --- check_out_time - on how much time user can take materials
class Patron(userBase):
    __metaclass__ = type

    def __init__(self, name, address, id, status,phone=None,history=None, current_books=None, check_out_time=None):
        userBase.__init__(self, name, address, status, id, phone)
        self.__history = history
        self.__current_books = current_books
        self.__check_out_time = check_out_time



    def get_history(self):
        return self.__history

    def get_info(self):
        return (self.get_id(),
                self.get_name(),
                self.get_address(),
                self.get_phone(),
                str(self.__history),
                str(self.__current_books),
                self.get_type())
