import sqlite3
from sqlite3 import Error
from UsersAndDocumentObjects.IBookingSystem import IBookingSystem
from UsersAndDocumentObjects.Document import Document
from UsersAndDocumentObjects.Librarian import Librarian
from UsersAndDocumentObjects.Patron import Patron
from UsersAndDocumentObjects.Patron import PatronType


class BDManagement:

    def __init__(self):
        file = 'DataBase.db'
        self.__create_connection(file)

    def __create_connection(self, file):
        try:
            self.__bd = sqlite3.connect(file)
            print(sqlite3.version)
            return self.__bd
        except Error as e:
            print(e)

    def __create_table(self, create_table_sql):
        try:
            c = self.__bd.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def __create_tables(self):

        self.__create_table(self.__bd, """
                CREATE TABLE IF NOT EXISTS librarians (
                id integer PRIMARY KEY,
                name text NOT NULL,
                phone integer,
                address text,
                type text
              ); """);

        self.__create_table(self.__bd, """
                 CREATE TABLE IF NOT EXISTS patrons (
                 id integer PRIMARY KEY,
                 name text NOT NULL,
                 phone integer,
                 address text,
                 history text,
                 current_books text,
                 type text
                  ); """);

        self.__create_table(self.__bd, """
              CREATE TABLE IF NOT EXISTS documents (
              id integer PRIMARY KEY,
              name text NOT NULL,
              description text NOT NULL,
              author text NOT NULL,
              count integer,
             free_count integer);
        """)
    def select_all(self):
        cur = self.__bd.cursor()
        cur.execute("SELECT * FROM patrons")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    def add_patron(self, newPatron):
        with self.__bd:
            sql = """ INSERT INTO patrons(id,name,address,phone,history,current_books,type)
                VALUES(?,?,?,?,?,?,?)"""
            cur = self.__bd.cursor()
            cur.execute(sql, newPatron.get_info())
        return cur.lastrowid
