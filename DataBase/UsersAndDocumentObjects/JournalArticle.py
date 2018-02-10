from DataBase.UsersAndDocumentObjects.BaseDoc import BaseDoc


# Class representing 'Article'
# Inherits from BaseDoc and adds new attributes: journal name,journal publisher
class JournalArticle(BaseDoc):
    def __init__(self,id, name, author, journal_name, journal_publisher, count, free_count, price,keywords):
        BaseDoc.__init__(self,id, author, name, count, free_count, price, "ARTICLE",keywords)
        self.journal_name = journal_name
        self.journal_publisher = journal_publisher
