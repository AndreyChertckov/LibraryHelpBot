
class userBase:
    # base class for all types of users:patrons,librarians and others

    def __init__(self, name, address, type, id, phone):
        self.set_name(name)
        self.set_address(address)
        self.set_phone(phone)
        self.__type = type
        self.__id = id

    # getting and setting name(returns true if name is suitable,false otherwise)
    def get_name(self):
        return str(self.__name)

    def set_name(self, name):
       # if any(char.isdigit() for char in str(name)):
       #     return False
        self.__name = name
        return True

    def get_type(self):
        return self.__type

    # setting and getting phone number
    def set_phone(self, phone):
        try:
            self.__phone_number = int(phone)
            return True
        except ValueError:
            return False

    def get_phone(self):
        return self.__phone_number

    # getting id
    def get_id(self):
        return self.__id

    # getting and setting adress
    def set_address(self, new_address):
        self.__address = new_address

    def get_address(self):
        return self.__address

    '''def get_history(self):
        return self.__history__
        ()
    '''
