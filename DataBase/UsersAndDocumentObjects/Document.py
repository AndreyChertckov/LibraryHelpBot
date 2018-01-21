# class representing all types of documents
class Document:
    def __init__(self, name, type, description, author, id, max_check_out_time, count, free_count):
        self.__name = name
        self.__descrtiption = description
        self.__type = type
        self.__author = author  # maybe useless
        self.__id = id
        self.__max_check_out_time = max_check_out_time
        self.__count = count
        self.__free_count = count

    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__type

    def edit_descriprion(self, desription):
        self.__descrtiption = desription

    def get_description(self):
        return self.__descrtiption

    def get_count(self):
        return self.__count

    def check_out(self):
        if (self.__free_count > 0):
            self.__free_count -= 1;
            return True
        else:
            return False

    def add_doc(self):
        self.__count += 1;
        self.__free_count += 1;

    def get_name(self):
        return self.__name

    # Позже добавить инфу о том кто вернул книгу(his id)
    def return_book(self):
        self.__free_count += 1;

    def get_info(self):
        print(self.__name+" "+self.__author+" "+self.__type+" "+self.get_description()+" "+str(self.get_count()));