from DataBase.UsersAndDocumentObjects.user import userBase


# Class representing 'Librarian' object
# Inherits from class 'UserBase'
class Librarian(userBase):
    __metaclass__ = type

    def __init__(self, name, address, id, phone, status):
        userBase.__init__(self, name, address, status, id, phone)

    def get_info(self):
        return (int(self.get_id()), self.get_name(), self.get_phone(), self.get_address(), self.get_type())
