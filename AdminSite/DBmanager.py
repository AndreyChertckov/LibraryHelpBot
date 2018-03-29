import pymysql
from configs import site_login_database,site_password_database, site_database

class DBManager:

    def __init__(self):
        self.db_connectionn = pymysql.connect('localhost',site_login_database,site_password_database,site_database,autocommit = True)
        self.init_tables()
    
    def init_tables(self):
        cur = self.db_connectionn.cursor()
        for sql in open('AdminSite/sql/tables-schema.sql').read().split('\n'):
            cur.execute(sql)

    def cleanup_database(self):
        cursor = self.db_connectionn.cursor()
        cursor.execute("DROP TABLE librarians;")
        cursor.execute('DROP TABLE sessions;')

    def get_user(self, login, hash_passwd):
        cursor = self.db_connectionn.cursor()
        cursor.execute("SELECT * FROM librarians WHERE login=%s AND password=%s;",(login,hash_passwd,))
        return cursor.fetchone()
    
    def create_user(self, user):
        cursor = self.db_connectionn.cursor()
        cursor.execute("INSERT INTO librarians(login,password,name,phone,address) VALUES (%s,%s,%s,%s,%s);",(user['login'],user['passwd'],user['name'],user['phone'],user['address'],))
    
    def get_user_id(self,login,hash_passwd):
        cursor = self.db_connectionn.cursor()
        cursor.execute("SELECT (id) FROM librarians WHERE login=%s AND password=%s;",(login,hash_passwd,))
        return cursor.fetchone()
    
    def create_session(self, session_id,user_id):
        cursor = self.db_connectionn.cursor()
        cursor.execute("INSERT INTO sessions VALUES (%s,%s);",(session_id,user_id,))
    
    def get_user_id_by_session(self, session_id):
        cursor = self.db_connectionn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE id=%s;",(session_id,))
        return cursor.fetchone()
    
    def delete_session(self, session_id):
        cursor = self.db_connectionn.cursor()
        cursor.execute("DELETE FROM sessions WHERE id=%s;",(session_id,))