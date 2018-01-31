from DataBase.UsersAndDocumentObjects.BaseDoc import BaseDoc


class JournalArticle(BaseDoc):
    def __init__(self, name, author, journal_name, journal_publisher, id, count, free_count, price):
        BaseDoc.__init__(self, id, author, name, count, free_count, price, "MEDIA")
        self.journal_name = journal_name
        self.journal_publisher = journal_publisher
