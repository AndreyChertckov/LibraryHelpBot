# class representing one order:
# It stores user id,which took some document in the library,and document id
from BDTables import BDTables
class OrderHistoryObject:

    def __init__(self,id,time,userId, docId):
        self.__userId = userId
        self.__docId = docId
        self.__time = time
        self.__id=id
        BDTables.bd.add_order(self)

    def get_info(self):
        return (self.__id,self.__time,self.__userId, self.__docId,)
