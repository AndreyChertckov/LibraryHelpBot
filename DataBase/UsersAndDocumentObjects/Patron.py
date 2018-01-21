from UsersAndDocumentObjects.IBookingSystem import IBookingSystem
from UsersAndDocumentObjects.user import userBase
from enum import Enum


# некоторый костыль(передалать их в классы)
class PatronType(Enum):
    student = 1
    proffessor = 2


class Patron(userBase, IBookingSystem):
    __metaclass__ = type

    def __init__(self, name, address, type, id, phone, history, current_books, check_out_time):
        userBase.__init__(self,name,address,type,id,phone)
        self.__history = history
        self.__current_books = current_books
        self.__check_out_time = check_out_time

    def get_history(self):
        return self.__history

    # IBookingSystem interface implementation
    def take_book(self, bookId): pass

    def return_book(self, bookId): pass

    def get_info(self):
        print(self.get_name() + " " + str(self.get_address()) + " " + str(self.get_phone()) + " " + str(self.get_type()))
