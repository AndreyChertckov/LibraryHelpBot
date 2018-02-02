import sqlite3
import ast
from sqlite3 import Error

'''
Features:
add_librarian
add_patron
add_document
select_all - get all data from custon table('patrons','librarians','documents')
delete_lable (deleteFrom,id) - delete cell with 'id' from 'deleteFrom' table
drop_table - deletes table
clear_table - clears table
'''


class BDManagement:
    def __init__(self):
        self.file = 'DataBase.db'
        #self.drop_table("orders")
        #self.__bd.cursor().execute("DROP TABLE articles")
        self.__create_tables()

    #        self.__bd.cursor().execute("DROP TABLE documents")


    # InnopolisUDj9^]Ye[

    # patron id name phone address history current_books
    # librarian id name phone address type
    # document id name author description type count free_count
    def select_all(self, table_to_select):
        cur = self.__create_connection(self.file).cursor()
        cur.execute("SELECT * FROM " + str(table_to_select));
        rows = cur.fetchall()
        print("Table " + table_to_select + ":");
       #for row in rows:
        #    print(row)
        return rows

    def add_chat(self, newChat):
        sql = """INSERT INTO chats(chat_id,table_,id) VALUES(?,?,?)"""
        self.__add_new(sql, newChat)

    def add_order(self, newOrder):
        sql = """INSERT INTO orders(id,date,storing_table,doc_id,user_id) VALUES(?,?,?,?,?)"""
        self.__add_new(sql, newOrder)

    def add_librarian(self, newLibr):
        sql = """INSERT INTO librarians(id,name,phone,address,type)
                    VALUES(?,?,?,?,?)"""
        self.__add_new(sql, newLibr)

    def select_label(self,selecting_table,id):
        return  self.__create_connection(self.file).cursor().execute("SELECT * FROM "+selecting_table+" WHERE id=?",(id,)).fetchone()

    # добавить в базу картеж в виде (id,name,author,descr.,type,count,free_count
    def add_document(self, newDoc):
        sql = """INSERT INTO books(id,name,author,description,count,free_count,price)
            VALUES (?,?,?,?,?,?,?)"""

        cur = self.__create_connection(self.file).cursor()
        cur.execute(sql,
                        (newDoc.id, newDoc.name, newDoc.authors, newDoc.description, newDoc.count, newDoc.free_count,
                         newDoc.price,))
            # self.__add_new(sql,(newDoc.id,newDoc.name))

    def add_media(self, newMed):
        sql = """INSERT INTO media(id,name,authors,type,count,free_count,price)
        VALUES(?,?,?,?,?,?,?)"""
        self.__bd.cursor().execute(sql, (
        newMed.id, newMed.name, newMed.authors, newMed.type, newMed.count, newMed.free_count, newMed.price))

    def add_article(self, newArticle):
        sql = """INSERT INTO articles(id,name,authors,journal_name,journal_publisher,count,free_count,price)
        VALUES(?,?,?,?,?,?,?,?)"""
        cur = self.__bd.cursor()  # cursor()

        cur.execute(sql, (newArticle.id, newArticle.name, newArticle.authors,newArticle.journal_name,
                          newArticle.journal_publisher, newArticle.count, newArticle.free_count, newArticle.price,))

    def add_patron(self, newPatron):
        sql = """ INSERT INTO patrons(id,name,address,phone,history,current_books,type)
                VALUES (?,?,?,?,?,?,?)"""
        self.__add_new(sql, newPatron)

    def edit_label(self, table, set, newLabel):
        sql = "UPDATE " + table + " SET " + set + " where id=?"
        cur = self.__create_connection(self.file).cursor()
        cur.execute(sql, newLabel)

    def delete_label(self, deleteFrom, deLID):
        self.__create_connection(self.file).cursor().execute("DELETE FROM " + deleteFrom + " where id=?", (deLID,))

    def clear_table(self, table):
        self.__create_connection(self.file).cursor().execute(table)

    def drop_table(self, table):
        self.__create_connection(self.file).cursor().execute("DROP TABLE IF EXISTS " + table)

    def __create_connection(self, file):
        try:
            return sqlite3.connect(self.file, isolation_level=None)
        except Error as e:
            print(e)

    def __create_table(self, create_table_sql):
        try:
            #c = self.__bd.cursor()
            c = self.__create_connection(self.file).cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def __create_tables(self):

        self.__create_table("""
                CREATE TABLE IF NOT EXISTS librarians (
                id integer PRIMARY KEY,
                name text NOT NULL,
                phone integer,
                address text,
                type text
              ); """);

        self.__create_table("""
                 CREATE TABLE IF NOT EXISTS patrons (
                 id integer PRIMARY KEY,
                 name text NOT NULL,
                 phone integer,
                 address text,
                 history text,
                 current_books text,
                 type text
                  ); """);

        self.__create_table("""
              CREATE TABLE IF NOT EXISTS books(
              id integer PRIMARY KEY,
              name text NOT NULL,
              author text NOT NULL,
              description text NOT NULL,
              count integer,
             free_count integer,
             price);
        """)
        self.__create_table("""CREATE TABLE IF NOT EXISTS articles(
             id integer PRIMARY KEY,
             name text NOT NULL,
             authors text,
            journal_name text,
            journal_publisher text,
            count integer,
            free_count integer,
            price);
        """)
        self.__create_table("""CREATE TABLE IF NOT EXISTS media(
                id integer PRIMARY KEY,
                name text NOT NULL,
                authors text,
                type text,
                count integer,
                free_count integer,
                price);
                """)
        self.__create_table("""
            CREATE TABLE IF NOT EXISTS chats (
            chat_id integer PRIMARY KEY,
            table_ text NOT NULL,
            id integer);
        """)

        self.__create_table("""
             CREATE TABLE  IF NOT EXISTS orders (
             id integer PRIMARY KEY,
             date text NOT NULL,
             storing_table text,
             doc_id integer,
             user_id integer,
             FOREIGN KEY (user_id) REFERENCES patrons (id)
             );
        """)

    # kek
    def __add_new(self, sql, new):
        cur = self.__create_connection(self.file).cursor()
        cur.execute(sql, new.get_info())
        return cur.lastrowid
