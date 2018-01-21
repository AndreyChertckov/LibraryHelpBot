# class representing one order:
# It stores user id,which took some document in the library,and document id
class OrderHistoryObject:

    def __init__(self, userId, docId, time):
        self.__userId = userId
        self.__docId = docId
        self.__time = time

    def get_info(self):
        return (self.__userId, self.__docId, self.__time,)
