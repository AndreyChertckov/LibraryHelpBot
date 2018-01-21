import abc


class IBookingSystem:
    @abc.abstractmethod
    def take_book(self, bookId): pass

    @abc.abstractmethod
    def return_book(self, bookId): pass
