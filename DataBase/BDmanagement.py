import sqlite3
from sqlite3 import Error


# Class,for saving data in the database,
# and obtaining it

# existing tables:
# ---patrons
# ---librarians
# ---chats - table containing chat id and type of the users
# ---articles
# ---media
# ---orders - table for keeping order history
# ---books
# ---unconfirmed - table containing new unconfirmed users

class BDManagement:
    # initializion of object
    def __init__(self):
        self.file = 'DataBase.db'

        self.__create_tables()

    # Get all data from some table
    # params:
    # ----table_to_select - name of the table to get information
    # returns number of the last row in the table
    def select_all(self, table_to_select):
        cur = self.__create_connection(self.file).cursor()
        cur.execute("SELECT * FROM " + str(table_to_select));
        rows = cur.fetchall()
        print("Table " + table_to_select + ":");
        return rows

    # Add new chat to DB
    # params:
    # ---newChat -  'Chat' Object

    def add_chat(self, newChat):
        sql = """INSERT INTO chats(chat_id,table_,id) VALUES(?,?,?)"""
        self.__add_new(sql, newChat)

    # Add new order to DB
    # params:
    #  ---newOrder -  'Order' Object

    def add_order(self, newOrder):
        sql = """INSERT INTO orders(id,date,storing_table,doc_id,user_id) VALUES(?,?,?,?,?)"""
        self.__add_new(sql, newOrder)

    # Add new Librarian to DB
    # params:
    #  ---newLibr -  'Librarian' Object

    def add_librarian(self, newLibr):
        sql = """INSERT INTO librarians(id,name,phone,address,type)
                    VALUES(?,?,?,?,?)"""
        self.__add_new(sql, newLibr)

    # Add new unconfirmed user to DB
    # params:
    #  ---newLibr -  'Librarian' Object (because unconfirmed user has the same attributes
    # like librarians

    def add_unconfirmed(self, newLibr):
        sql = """INSERT INTO unconfirmed(id,name,phone,address,type)
                    VALUES(?,?,?,?,?)"""
        self.__add_new(sql, newLibr)

    # Select some label
    # params:
    #  ---selecting_table - name of the table to select from
    #  ---id - id of the record
    # returns:cortege with all attributes

    def select_label(self, selecting_table, id):
        return self.__create_connection(self.file).cursor().execute("SELECT * FROM " + selecting_table + " WHERE id=?",
                                                                    (id,)).fetchone()

    # Add new  book to DB
    #  params:
    #  ---newDoc -  'Document' Object

    def add_document(self, newDoc):
        sql = """INSERT INTO books(id,name,author,description,count,free_count,price)
            VALUES (?,?,?,?,?,?,?)"""

        cur = self.__create_connection(self.file).cursor()
        cur.execute(sql,
                    (self.get_max_id("books")+1, newDoc.name, newDoc.authors, newDoc.description, newDoc.count, newDoc.free_count,
                     newDoc.price,))

    # Add new media to DB
    # params:
    # ---newMed - 'Media' object

    def add_media(self, newMed):
        sql = """INSERT INTO media(id,name,authors,type,count,free_count,price)
        VALUES(?,?,?,?,?,?,?)"""
        self.__bd.cursor().execute(sql, (
            self.get_max_id("media") + 1, newMed.name, newMed.authors, newMed.type, newMed.count, newMed.free_count, newMed.price))

    # Add new article to DB
    # params:
    # --- newArticle - 'JournalArticle' object

    def add_article(self, newArticle):
        sql = """INSERT INTO articles(id,name,authors,journal_name,journal_publisher,count,free_count,price)
        VALUES(?,?,?,?,?,?,?,?)"""
        cur = self.__bd.cursor()  # cursor()

        cur.execute(sql, (self.get_max_id("articles")+1, newArticle.name, newArticle.authors, newArticle.journal_name,
                          newArticle.journal_publisher, newArticle.count, newArticle.free_count, newArticle.price,))

    # Add new 'patron' to DB
    # params:
    # ---newPatron - 'Patron' object
    def add_patron(self, newPatron):
        sql = """ INSERT INTO patrons(id,name,address,phone,history,current_books,type)
                VALUES (?,?,?,?,?,?,?)"""
        self.__add_new(sql, newPatron)

    # Updates some record
    # params:
    # ---table - table to update record from(string)
    # ---set - what to update(string)
    # ---newLabel - cortege , containing updated information
    def edit_label(self, table, set, newLabel):
        sql = "UPDATE " + table + " SET " + set + " where id=?"
        cur = self.__create_connection(self.file).cursor()
        cur.execute(sql, newLabel)

    # Deletes some record
    # params:
    # ---deleteFrom - table to delete from(string)
    # ---delID - id of the record to delete

    def delete_label(self, deleteFrom, deLID):
        self.__create_connection(self.file).cursor().execute("DELETE FROM " + deleteFrom + " where id=?", (deLID,))

    # Clears some table
    # params:
    # ---table - table to clear(string)
    def clear_table(self, table):
        self.__create_connection(self.file).cursor().execute(table)

    # Deletes some table
    # params:
    # ---table - table to delete(string)

    def drop_table(self, table):
        self.__create_connection(self.file).cursor().execute("DROP TABLE IF EXISTS " + table)

    # Get connection to the database
    def __create_connection(self, file):
        try:
            return sqlite3.connect(self.file, isolation_level=None)
        except Error as e:
            print(e)

    # Execute sql query to create new table:
    # params:
    # ----create_table_sql - sql query(string)
    def __create_table(self, create_table_sql):
        try:
            # c = self.__bd.cursor()
            c = self.__create_connection(self.file).cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    # Create all tables
    def __create_tables(self):

        self.__create_table("""
                CREATE TABLE IF NOT EXISTS librarians (
                id integer PRIMARY KEY,
                name text NOT NULL,
                phone text,
                address text,
                type text
              ); """);
        self.__create_table("""
                        CREATE TABLE IF NOT EXISTS unconfirmed (
                        id integer PRIMARY KEY,
                        name text NOT NULL,
                        phone text,
                        address text,
                        type text
                      ); """);
        self.__create_table("""
                 CREATE TABLE IF NOT EXISTS patrons (
                 id integer PRIMARY KEY,
                 name text NOT NULL,
                 phone text,
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
             price integer);
        """)
        self.__create_table("""CREATE TABLE IF NOT EXISTS articles(
             id integer PRIMARY KEY,
             name text NOT NULL,
             authors text,
            journal_name text,
            journal_publisher text,
            count integer,
            free_count integer,
            price integer);
        """)
        self.__create_table("""CREATE TABLE IF NOT EXISTS media(
                id integer PRIMARY KEY,
                name text NOT NULL,
                authors text,
                type text,
                count integer,
                free_count integer,
                price integer);
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

    # Add new record to the database
    # params:
    # ---sql - sql command for adding new record
    # ---new - new record
    def __add_new(self, sql, new):
        cur = self.__create_connection(self.file).cursor()
        cur.execute(sql, new.get_info())
        return cur.lastrowid

    def get_max_id(self, table):
        a = self.__create_connection(self.file).execute("SELECT max(id) from " + table).fetchone()[0]
        if (a == None):
            return 0;
        else:
            return a;
