class userBase:
    # base class for all types of users:patrons,librarians and others

    def __init__(self, name, address, type, id, phone):
        self.set_name(name)
        self.set_address(address)
        self.set_phone(phone)
        self.__type = type
        self.__id = id

    # get name
    def get_name(self):
        return str(self.__name)

    # set name
    def set_name(self, name):
        self.__name = name
        return True

    # get type
    def get_type(self):
        return self.__type

    # setting and getting phone number
    def set_phone(self, phone):
        self.__phone_number = phone

    # get phone
    def get_phone(self):
        return self.__phone_number

    # getting id
    def get_id(self):
        return self.__id

    # getting and setting adress
    def set_address(self, new_address):
        self.__address = new_address

    # getting address
    def get_address(self):
        return self.__address
