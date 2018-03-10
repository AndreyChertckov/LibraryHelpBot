import pymysql
from configs import site_login_databse,site_password_database, site_database

class DBManager:

    def __init__(self):
        self.db_connectionn = pymysql.connect('localhost',site_login_databse,site_password_database,site_database)
        self.init_tables()
    
    def init_tables(self):
        cur = self.db_connectionn.cursor()
        for sql in open('AdminSite/sql/tables-schema.sql').read().split('\n'):
            cur.execute(sql)

    def get_user(self, login, hash_passwd):
        cursor = self.db_connectionn.cursor()
        cursor.execute("SELECT * FROM librarians WHERE login=%s AND password=%s",(login,hash_passwd,))
        return cursor.fetchone()