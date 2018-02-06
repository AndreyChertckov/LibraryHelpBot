# class representing one order:
# It stores user id,which took some document in the library,and document id

class OrderHistoryObject:
    def __init__(self, id, time, table, userId, docId):
        self.userId = userId
        self.docId = docId
        self.time = time
        self.id = id
        self.table = table

    def get_info(self):
        return (self.id, self.time, self.table, self.docId, self.userId,)
