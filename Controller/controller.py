from DataBase.BDmanagement import BDManagement
from DataBase.UsersAndDocumentObjects.Patron import Patron
from DataBase.UsersAndDocumentObjects.Librarian import Librarian
from DataBase.UsersAndDocumentObjects.Document import Document
from DataBase.UsersAndDocumentObjects.OrderHistory import OrderHistoryObject
from DataBase.UsersAndDocumentObjects.JournalArticle import JournalArticle
from DataBase.UsersAndDocumentObjects.BaseDoc import BaseDoc


class Controller:
    def __init__(self):
        self.BDmanager = BDManagement()

    def confirm_user(self, id):
        x = self.BDmanager.select_label("unconfirmed", id)
        l = Librarian(x[1], x[3], x[0], x[2], x[4])
        self.delete_unconfirmed_user(id)
        self.BDmanager.add_patron(Patron(l.get_name(), l.get_address(), id, l.get_phone(), [], [], 2))

    def delete_unconfirmed_user(self, id):
        self.BDmanager.delete_label("unconfirmed", id)

    def registration(self, user_info):
        unconfirmed_patron = Librarian(**user_info)
        self.BDmanager.add_unconfirmed(unconfirmed_patron)

    def delete_user(self, user_info):
        print(self.remove_user(user_info['id'], 'librarians' if user_info['status'] == "Librarian" else 'patrons'))

    def get_all_patrons(self):
        rows = self.BDmanager.select_all("patrons")
        return [{'name':user[1], 'address':user[3], 'id': user[0], 'phone':user[2], 'history':user[4], 'current_books':user[5], 'check_out_time':2} for user in rows]

    def get_all_librarians(self):
        rows = self.BDmanager.select_all("librarians")
        return [{'name':user[1], 'address':user[3], 'id':user[0], 'phone':user[2], 'status':user[4]} for user in rows]

    def get_all_unconfirmed(self):
        rows = self.BDmanager.select_all("unconfirmed")
        return [{'name':user[1], 'address':user[3], 'id':user[0], 'phone':user[2], 'status':user[4]} for user in rows]

    def get_all_books(self):
        rows = self.BDmanager.select_all("books")
        return [Document(book[1], book[3], book[2], book[0], book[4], book[5], book[6]) for book in rows]

    def get_all_articles(self):
        rows = self.BDmanager.select_all("articles")
        return [JournalArticle(article[1], article[2], article[3], article[4], article[0], article[5], article[6], article[7]) for article in rows]

    def get_all_media(self):
        rows = self.BDmanager.select_all("media")
        return [BaseDoc(media[0], media[2], media[1], media[4], media[5], media[6], media[3]) for media in rows]

    def chat_exists(self, id):
        return any([self.BDmanager.select_label('librarians', id), self.BDmanager.select_label('patrons', id)])

    def remove_user(self, id, table=None):
        if table != None:
            if self.BDmanager.select_label(table, id):
                self.BDmanager.delete_label(table, id)
                return True
            else:
                return False
        else:
            if self.BDmanager.select_label('librarians', id):
                self.BDmanager.delete_label('librarians', id)
                return True
            elif self.BDmanager.select_label('patrons', id):
                self.BDmanager.delete_label('patrons', id)
                return True
            else:
                return False

    def get_user(self, id):
        user = {}
        if self.BDmanager.select_label('patrons', id):
            user_bd = self.BDmanager.select_label('patrons', id)
            user['id'] = user_bd[0]
            user['name'] = user_bd[1]
            user['address'] = user_bd[2]
            user['phone'] = user_bd[3]
            user['history'] = user_bd[4]
            user['current_books'] = user_bd[5]
            user['status'] = user_bd[6]
        elif self.BDmanager.select_label('librarians', id):
            user_bd = self.BDmanager.select_label('librarians', id)
            user['id'] = user_bd[0]
            user['name'] = user_bd[1]
            user['phone'] = user_bd[2]
            user['address'] = user_bd[3]
            user['status'] = user_bd[4]
        else:
            return False
        return user

    def upto_librarian(self, user_id):
        user_info = self.get_user(user_id)
        self.remove_user(user_id, 'patrons')
        user_info["status"] = 'librarian'
        librarian = Librarian(user_info['name'], user_info['address'], user_info['id'], user_info['phone'], 'librarian')
        self.BDmanager.add_librarian(librarian)

    # Функция должна возвращать от 0 до 3 в зависимости от того, в какой таблице пользователь
    def user_type(self, user_id):
        d = {"unauthorized": 0, 'unconfirmed': 1, 'patron': 2, 'admin': 3}
        if self.BDmanager.select_label('librarians', user_id):
            return d['admin']
        elif self.BDmanager.select_label('patrons',user_id):
            return d['patron']
        elif self.BDmanager.select_label('unconfirmed',user_id):
            return d['unconfirmed']
        else:
            return d['unauthorized']
