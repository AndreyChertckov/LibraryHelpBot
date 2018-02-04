from DataBase.UsersAndDocumentObjects.BaseDoc import BaseDoc


# Class representing 'BOOK'
# Inherits from BaseDoc and adds new attribute:description
class Document(BaseDoc):
    def __init__(self, name, description, author, count, free_count, price):
        BaseDoc.__init__(self, author, name, count, free_count, price, "BOOK")
        self.description = description
