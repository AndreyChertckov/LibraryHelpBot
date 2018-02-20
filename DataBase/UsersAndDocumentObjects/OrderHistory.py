# class representing one order:
# It stores user id,which took some document in the library,and document id

class OrderHistoryObject:
    def __init__(self,time, table, userId, docId,active=1,out_of_time=None):
        self.userId = userId
        self.docId = docId
        self.time = time
        self.table = table
        self.out_of_time=out_of_time
        self.active=active
    def get_info(self):
        return (self.time, self.table, self.docId, self.userId,self.out_of_time,self.active)
