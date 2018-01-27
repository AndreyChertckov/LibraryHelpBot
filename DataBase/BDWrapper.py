import sqlite3

from DataBase.UsersAndDocumentObjects.Librarian import Librarian
from DataBase.UsersAndDocumentObjects.Patron import Patron
from DataBase.UsersAndDocumentObjects.OrderHistory import OrderHistoryObject
from DataBase.BDmanagement import BDManagement
from DataBase.BDTables import BDTables
from DataBase.UsersAndDocumentObjects.Document import Document
from DataBase.UsersAndDocumentObjects.Patron import PatronType
from DataBase.UsersAndDocumentObjects.Chat import chat

class BDWrapper:

    def __init__(self):
        self.__bd = BDTables.bd

    def get_all_patrons(self):
        rows = BDTables.bd.select_all("patrons")
        return [Patron(x[1], x[3], "patron", x[0], x[2], x[4], x[5], 2) for x in rows]

    def get_all_librarians(self):
        rows = BDTables.bd.select_all("librarians")
        return [Librarian(x[1], x[3], x[0], x[2]) for x in rows]

    def get_all_documents(self):
        rows = BDTables.bd.select_all("documents")
        return [Document(x[1], x[4], x[3], x[2], x[0], 2, x[5], x[6]) for x in rows]

    def get_all_chats(self):
        rows=BDTables.bd.select_all("chats")
        return [chat(x[0], x[1], x[2]) for x in rows]

    def chat_exists(self, id):
        return any(x.get_chat_id()==id for x in self.get_all("chats"))

    def add_chat(self, chat_id, table):
        chat(chat_id,table,chat_id).load()

