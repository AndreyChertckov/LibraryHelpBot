# class representing one order:
# It stores user id,which took some document in the library,and document id

class OrderHistoryObject:
    def __init__(self, id, time, table, userId, docId):
        self.__userId = userId
        self.__docId = docId
        self.__time = time
        self.__id = id
        self.__table = table

    def get_info(self):
        return (self.__id, self.__time, self.__table, self.__docId, self.__userId,)
