import sqlite3
from sqlite3 import Error



class BDManagement:

    def __init__(self):
        file = 'DataBase.db'
        self.__create_connection(file)
        self.__create_tables()
        #self.__bd.cursor().execute("DROP TABLE documents")
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

        self.__create_table( """
                CREATE TABLE IF NOT EXISTS librarians (
                id integer PRIMARY KEY,
                name text NOT NULL,
                phone integer,
                address text,
                type text
              ); """);

        self.__create_table( """
                 CREATE TABLE IF NOT EXISTS patrons (
                 id integer PRIMARY KEY,
                 name text NOT NULL,
                 phone integer,
                 address text,
                 history text,
                 current_books text,
                 type text
                  ); """);

        self.__create_table( """
              CREATE TABLE IF NOT EXISTS documents (
              id integer PRIMARY KEY,
              name text NOT NULL,
              author text NOT NULL,
              description text NOT NULL,
              type text,
              count integer,
             free_count integer);
        """)

    def select_all(self,table_to_select):
        cur = self.__bd.cursor()
        cur.execute("SELECT * FROM "+str(table_to_select));
        rows = cur.fetchall()
        print("Table "+table_to_select+":");
        for row in rows:
            print(row)

    def add_librarian(self,newLibr):
            sql="""INSERT INTO librarians(id,name,phone,address,type)
                    VALUES(?,?,?,?,?)"""
            self.__add_new(sql,newLibr)

    # добавить в базу картеж в виде (id,name,author,descr.,type,count,free_count
    def add_document(self,newDoc):
            sql="""INSERT INTO documents(id,name,author,description,type,count,free_count)
            VALUES (?,?,?,?,?,?,?)"""
            self.__add_new(sql,newDoc)

    def add_patron(self, newPatron):
            sql = """ INSERT INTO patrons(id,name,address,phone,history,current_books,type)
                VALUES (?,?,?,?,?,?,?)"""
            self.__add_new(sql,newPatron)

    def __add_new(self,sql,new):
        with self.__bd:
            cur = self.__bd.cursor()
            print(new.get_info())
            cur.execute(sql, new.get_info())
        return cur.lastrowid

