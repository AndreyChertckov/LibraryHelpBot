import sqlite3

from DataBase.UsersAndDocumentObjects.Librarian import Librarian
from DataBase.UsersAndDocumentObjects.Patron import Patron
from DataBase.UsersAndDocumentObjects.OrderHistory import OrderHistoryObject
from DataBase.BDmanagement import BDManagement
from DataBase.BDTables import BDTables
from DataBase.UsersAndDocumentObjects.Document import Document
from DataBase.UsersAndDocumentObjects.Patron import PatronType
from DataBase.UsersAndDocumentObjects.Chat import chat
from DataBase.UsersAndDocumentObjects.BaseDoc import BaseDoc
from DataBase.UsersAndDocumentObjects.JournalArticle import JournalArticle
class BDWrapper:

    def __init__(self):
        self.__bd = BDTables.bd

    def get_all_patrons(self):
        rows = BDTables.bd.select_all("patrons")
        return [Patron(x[1], x[3], "patron", x[0], x[2], x[4], x[5], 2) for x in rows]

    def get_all_librarians(self):
        rows = BDTables.bd.select_all("librarians")
        return [Librarian(x[1], x[3], x[0], x[2]) for x in rows]

    def get_all_books(self):
        rows = BDTables.bd.select_all("books")
        return [Document(x[1],x[3],x[2],x[0],x[4],x[5],x[6]) for x in rows]

    def get_all_articles(self):
       rows=BDTables.bd.select_all("articles")
       return [JournalArticle(x[1],x[2],x[3],x[4],x[0],x[5],x[6],x[7]) for x in rows]

    def get_all_media(self):
        rows=BDTables.bd.select_all("media")
        return [BaseDoc(x[0],x[2],x[1],x[4],x[5],x[6],x[3])for x in rows]

    def get_all_chats(self):
        rows=BDTables.bd.select_all("chats")
        return [chat(x[0], x[1], x[2]) for x in rows]

    def chat_exists(self, id):
        return any(x.get_chat_id()==id for x in self.get_all("chats"))

    def add_new_user(self,obj):
        if (obj[1]["status"]=="faculty" or
                obj[1]["status"]=="student"):
            p=Patron(obj[1]["name"],obj[1]["address"],obj[1]["status"],obj[0],obj[1]["phone"],[],[],3)
            self.__bd.add_patron(p)
        else:
            l=Librarian(obj[1]["name"],obj[1]["address"],obj[0],obj[1]["phone"])
            self.__bd.add_librarian(l)

    def add_chat(self, chat_id, table):
        chat(chat_id,table,chat_id).load()

