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
        file = 'DataBase.db'
        self.__create_connection(file)
        self.__create_tables()
        # self.__bd.cursor().execute("DROP TABLE documents")
#InnopolisUDj9^]Ye[

    #patron id name phone address history current_books
    #librarian id name phone address type
    #document id name author description type count free_count
    def select_all(self, table_to_select):
        cur = self.__bd.cursor()
        cur.execute("SELECT * FROM " + str(table_to_select));
        rows = cur.fetchall()
        print("Table " + table_to_select + ":");
        for row in rows:
            print(row)
        return rows

    def add_librarian(self, newLibr):
        sql = """INSERT INTO librarians(id,name,phone,address,type)
                    VALUES(?,?,?,?,?)"""
        self.__add_new(sql, newLibr)

    # добавить в базу картеж в виде (id,name,author,descr.,type,count,free_count
    def add_document(self, newDoc):
        sql = """INSERT INTO documents(id,name,author,description,type,count,free_count)
            VALUES (?,?,?,?,?,?,?)"""
        self.__add_new(sql, newDoc)

    def add_patron(self, newPatron):
        sql = """ INSERT INTO patrons(id,name,address,phone,history,current_books,type)
                VALUES (?,?,?,?,?,?,?)"""
        self.__add_new(sql, newPatron)

    def edit_label(self, table, set, newLabel):
        sql = "UPDATE " + table + " SET " + set + " where id=?"
        cur = self.__bd.cursor()
        cur.execute(sql, newLabel)

    def delete_label(self, deleteFrom, deLID):
        self.__bd.cursor().execute("DELETE FROM "+deleteFrom+" where id=?",(deLID,))

    def clear_table(self,table):
        self.__bd.cursor().execute("")

    def drop_table(self, table):
        self.__bd.cursor().execute("DROP TABLE IF EXISTS " + table)

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
              CREATE TABLE IF NOT EXISTS documents (
              id integer PRIMARY KEY,
              name text NOT NULL,
              author text NOT NULL,
              description text NOT NULL,
              type text,
              count integer,
             free_count integer);
        """)

    def __add_new(self, sql, new):
        with self.__bd:
            cur = self.__bd.cursor()

            cur.execute(sql, new.get_info())
        return cur.lastrowid
