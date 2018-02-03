from DataBase.UsersAndDocumentObjects.BaseDoc import BaseDoc


class Document(BaseDoc):
    def __init__(self, name, description, author, id, count, free_count, price):
        BaseDoc.__init__(self, id, author, name, count, free_count, price, "BOOK")
        self.description = description
