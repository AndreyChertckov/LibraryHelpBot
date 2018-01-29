from BDTables import BDTables
from UsersAndDocumentObjects.BaseDoc import BaseDoc
# class representing all types of documents
class Document(BaseDoc):
    def __init__(self, name, description, author, id, count, free_count,price):
        BaseDoc.__init__(self,id,author,name,count,free_count,price,"BOOK")
        self.description = description
