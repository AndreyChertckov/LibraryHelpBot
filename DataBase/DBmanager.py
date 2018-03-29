import pymysql
from configs import site_login_databse,site_password_database, site_database


# Class,for saving data in the database,
# and obtaining it

# existing tables:
# ---patrons
# ---librarians
# ---article
# ---media
# ---orders - table for keeping order history
# ---book
# ---unconfirmed - table containing new unconfirmed users

class Manager:
    # initializion of object
    def __init__(self):
        # self.drop_table("orders")

        self.db_connectionn = pymysql.connect('localhost', site_login_databse, site_password_database, site_database,
                                          autocommit=True)
       # self.drop_tables()
        self.__create_tables()

    # Get all data from some table
    # params:
    # ----table_to_select - name of the table to get information
    # returns number of the last row in the table

    def drop_tables(self):
        self.drop_table('book')
        self.drop_table('orders')
        self.drop_table('patrons')
        self.drop_table('article')
        self.drop_table('media')
        self.drop_table('unconfirmed')

    def select_all(self, table_to_select):
        cur = self.__create_connection().cursor()
        cur.execute("SELECT * FROM " + str(table_to_select))
        rows = cur.fetchall()
        return rows

    # Add new order to DB
    # params:
    #  ---newOrder -  'Order' Object

    def add_order(self, newOrder):
        sql = """INSERT INTO orders(date,storing_table,doc_id,user_id,out_of_time,active) 
        VALUES(%s,%s,%s,%s,%s,%s)"""
        self.add_new(sql, (newOrder.date, newOrder.table, newOrder.doc_id,
                           newOrder.user_id, newOrder.out_of_time, newOrder.active))

    # Add new Librarian to DB
    # params:
    #  ---newLibr -  'Librarian' Object

    def add_librarian(self, newLibr):
        sql = """INSERT INTO librarians(id,name,phone,address)
                    VALUES(%s,%s,%s,%s)"""
        self.add_new(sql, (newLibr.id, newLibr.name, newLibr.phone, newLibr.address))

    # Add new unconfirmed user to DB
    # params:
    #  ---newLibr -  'Librarian' Object (because unconfirmed user has the same attributes
    # like librarians

    def add_unconfirmed(self, unconf):
        sql = """INSERT INTO unconfirmed(id,name,phone,address,status)
                    VALUES(%s,%s,%s,%s,%s)"""
        self.add_new(sql, (unconf.id, unconf.name, unconf.phone, unconf.address, unconf.status))

    # Select some label
    # params:
    #  ---selecting_table - name of the table to select from
    #  ---id - id of the record
    # returns:cortege with all attributes

    def select_label(self, selecting_table, id):
        cur=self.__create_connection().cursor()
        cur.execute("SELECT * FROM " + selecting_table + " WHERE id="+str(id)+";")
        a=cur.fetchone()
        return a
    # Add new  book to DB
    #  params:
    #  ---newDoc -  'Document' Object

    def add_book(self, newDoc):
        sql = """INSERT INTO book(title,authors,description,count,free_count,price,best_seller,keywords,queue)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        cur = self.__create_connection().cursor()
        self.add_new(sql, (newDoc.title, newDoc.authors, newDoc.description, newDoc.count, newDoc.free_count,
                           newDoc.price, newDoc.best_seller, newDoc.keywords,'[[],[],[],[],[]]'))

    # Add new media to DB
    # params:
    # ---newMed - 'Media' object

    def add_media(self, newMed):
        sql = """INSERT INTO media(title,authors,count,free_count,price,keywords,queue)
        VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        self.add_new(sql, (newMed.title, newMed.authors, newMed.count,
                           newMed.free_count, newMed.price, newMed.keywords,'[[],[],[],[],[]]'))

    # Add new article to DB
    # params:
    # --- newArticle - 'JournalArticle' object

    def add_article(self, newArticle):
        sql = """INSERT INTO article(title,authors,journal,count,free_count,price,keywords,issue,editors,date,queue)
        VALUES(%s,%s,%s,%i,%i,%i,%s,%s,%s,%s,%s)"""
        self.add_new(sql, (newArticle.title, newArticle.authors, newArticle.journal,
                           newArticle.count, newArticle.free_count, newArticle.price, newArticle.keywords,
                           newArticle.issue, newArticle.editors, newArticle.date,'[[],[],[],[],[]]'))

    # Add new 'patron' to DB
    # params:
    # ---newPatron - 'Patron' object
    def add_patron(self, newPatron):
        sql = """INSERT INTO patrons(id, name, address, phone, history, current_docs, status,queue) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        self.add_new(sql, (newPatron.id, newPatron.name, newPatron.address, newPatron.phone,
                           str(newPatron.history), str(newPatron.current_docs), newPatron.status,'[]'))

    # Updates some record
    # params:
    # ---table - table to update record from(string)
    # ---set - what to update(string)
    # ---newLabel - cortege , containing updated information
    def edit_label(self, table, sets, newLabels, id):
        sql = "UPDATE " + table + " SET " + ', '.join([set + '=%s' for set in sets]) + " WHERE id=%s"
        cur = self.__create_connection().cursor()
        cur.execute(sql, tuple(newLabels + [id]))

    # Deletes some record
    # params:
    # ---deleteFrom - table to delete from(string)
    # ---delID - id of the record to delete

    def delete_label(self, deleteFrom, deLID):
        self.__create_connection().cursor().execute("DELETE FROM " + deleteFrom + " where id=%s", (deLID,))

    # Clears some table
    # params:
    # ---table - table to clear(string)
    def clear_table(self, table):
        #self.__create_connection(self.file).cursor().execute("UPDATE sqlite_sequence SET seq=%s where name=%s",
        #                                                     (0, table,))
        self.__create_connection().cursor().execute("DELETE FROM " + table)

    # Deletes some table
    # params:
    # ---table - table to delete(string)

    def drop_table(self, table):
        self.__create_connection().cursor().execute("DROP TABLE IF EXISTS " + table)

    # Get connection to the database
    def __create_connection(self, file=None):
        return self.db_connectionn

    # Execute sql query to create new table:
    # params:
    # ----create_table_sql - sql query(string)
    def __create_table(self, create_table_sql):
            c = self.__create_connection().cursor()
            c.execute(create_table_sql)


    # Create all tables
    def __create_tables(self):

        self.__create_table("""
                CREATE TABLE IF NOT EXISTS librarians (
                id INTEGER PRIMARY KEY ,
                name TEXT NOT NULL,
                phone TEXT,
                address TEXT
              ); """)
        self.__create_table("""
                        CREATE TABLE IF NOT EXISTS unconfirmed (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        phone TEXT,
                        address TEXT,
                        status TEXT
                      ); """)
        self.__create_table("""
                 CREATE TABLE IF NOT EXISTS patrons (
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 phone TEXT,
                 address TEXT,
                 history TEXT,
                 current_docs TEXT,
                 status TEXT,
                 queue TEXT
                  ); """)

        self.__create_table("""CREATE TABLE IF NOT EXISTS book(
              id INTEGER AUTO_INCREMENT,
              title TEXT NOT NULL,
              authors TEXT NOT NULL,
              description TEXT NOT NULL,
              count INTEGER,
              free_count INTEGER,
              price INTEGER,
              best_seller INTEGER,
              keywords TEXT,
              queue TEXT,
              PRIMARY KEY(id)
              );
        """)
        self.__create_table("""CREATE TABLE IF NOT EXISTS article(
            id INTEGER  PRIMARY KEY AUTO_INCREMENT,
            title TEXT NOT NULL,
            authors TEXT,
            journal TEXT,
            count INTEGER,
            free_count INTEGER,
            price INTEGER,
            keywords TEXT,
            issue TEXT,
            editors TEXT,
            date TEXT,
            queue TEXT);
        """)
        self.__create_table("""CREATE TABLE IF NOT EXISTS media(
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                title TEXT NOT NULL,
                authors TEXT,
                count INTEGER,
                free_count INTEGER,
                price INTEGER,
                keywords TEXT,
                queue TEXT);
                """)
        self.__create_table("""
             CREATE TABLE  IF NOT EXISTS orders (
             id INTEGER PRIMARY KEY AUTO_INCREMENT,
             date TEXT NOT NULL,
             storing_table TEXT,
             doc_id INTEGER,
             user_id INTEGER,
             out_of_time TEXT,
             active INTEGER,
             FOREIGN KEY (user_id) REFERENCES patrons(id)
             );
        """)

    # Add new record to the database
    # params:
    # ---sql - sql command for adding new record
    # ---new - new record
    def add_new(self, sql, new):
        cur = self.__create_connection().cursor()
        cur.execute(sql , new)
        return cur.lastrowid

    def get_max_id(self, table):
        cur=self.__create_connection().cursor()
        cur.execute("SELECT max(id) from " + table)
        a=cur.fetchone()[0]
        return a if a else 0

    def get_by(self, get_by_what, get_from, get_value):
        sql = "SELECT * from " + get_from + " WHERE " + get_by_what + "=%s"
        cur=self.__create_connection().cursor()
        ans=cur.execute(sql,(get_value,))
        return cur.fetchall()

    def get_by_parameters(self, get_by_whats, get_from, get_values):
        sql = "SELECT * from " + get_from + " WHERE " + ' AND '.join([param + '=%s' for param in get_by_whats])
        cur=self.__create_connection().cursor()
        ans=cur.execute(sql,tuple(get_values))
        return cur.fetchall()

    def get_label(self, what_to_select, from_table, id):
        cur=self.__create_connection().cursor()
        cur.execute(
            "SELECT " + what_to_select + " from " + from_table + " WHERE id=" + str(id))
        a=cur.fetchone()[0]
        return a

    def get_count(self, table):
        cur=self.__create_connection().cursor()
        cur.execute("SELECT count(*) from " + table+";")
        a=cur.fetchone()[0]
        return a

    def get_connection(self):
        return self.db_connectionn.cursor()
            #return self.__create_connection(self.file).cursor()
