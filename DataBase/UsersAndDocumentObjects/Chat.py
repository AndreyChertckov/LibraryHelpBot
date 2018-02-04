# Class containing chat id,  type and table(where are they in DB) of the users
class chat:
    def __init__(self, chat_id, table, id):
        self.__chat_id = chat_id
        self.__id = id
        self.__table = table

    def get_chat_id(self):
        return self.__chat_id

    # Return cortege with all attributes
    def get_info(self):
        return (self.get_chat_id(), self.__table, self.__id)
