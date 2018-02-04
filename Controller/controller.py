from DataBase.BDmanagement import BDManagement
from DataBase.UsersAndDocumentObjects.Patron import Patron
from DataBase.UsersAndDocumentObjects.Librarian import Librarian
from DataBase.UsersAndDocumentObjects.Document import Document
from DataBase.UsersAndDocumentObjects.OrderHistory import OrderHistoryObject
from DataBase.UsersAndDocumentObjects.JournalArticle import JournalArticle
from DataBase.UsersAndDocumentObjects.BaseDoc import BaseDoc

#Class booking system
class Controller:
    

    def __init__(self):
        self.BDmanager = BDManagement()

    # Accept user to the library
    # param: user_id - id of user
    def confirm_user(self, user_id):
        user_data = self.BDmanager.select_label("unconfirmed", user_id)
        confirmed_user = Librarian(user[1], user[3], user[0], user[2], user[4])
        self.remove_user(user_id,'unconfirmed')
        self.BDmanager.add_patron(Patron(confirmed_user.get_name(), confirmed_user.get_address(), user_id, confirmed_user.get_phone(), [], [], 2))

    # Put user in queue for accepting to the library
    # param: user_info: dictionary {id,name,address,status,phone}
    def registration(self, user_info):
        unconfirmed_patron = Librarian(**user_info)
        self.BDmanager.add_unconfirmed(unconfirmed_patron)

    # Delete user by user_info
    # param: user_info: dictionary {id,name,address,status,phone}
    def delete_user(self, user_info):
        table = ['unauthorized', 'unconfirmed', 'patrons', 'librarians'][self.user_type(user_info['id'])]
        if table != 'unauthorized':
            self.remove_user(user_info['id'],table)


    # Return all patrons from database
    def get_all_patrons(self):
        rows = self.BDmanager.select_all("patrons")
        return [{'name':user[1], 'address':user[3], 'id': user[0], 'phone':user[2], 'history':user[4], 'current_books':user[5], 'check_out_time':2} for user in rows]


    # Return all librarians from database
    def get_all_librarians(self):
        rows = self.BDmanager.select_all("librarians")
        return [{'name':user[1], 'address':user[3], 'id':user[0], 'phone':user[2], 'status':user[4]} for user in rows]


    # Return all users who don`t confirmed
    def get_all_unconfirmed(self):
        rows = self.BDmanager.select_all("unconfirmed")
        return [{'name':user[1], 'address':user[3], 'id':user[0], 'phone':user[2], 'status':user[4]} for user in rows]


    # Return all books from database
    def get_all_books(self):
        rows = self.BDmanager.select_all("books")
        return [Document(book[1], book[3], book[2], book[0], book[4], book[5], book[6]) for book in rows]


    # Return all articles from database
    def get_all_articles(self):
        rows = self.BDmanager.select_all("articles")
        return [JournalArticle(article[1], article[2], article[3], article[4], articledatabase[0], article[5], article[6], article[7]) for article in rows]


    # Return all media from database
    def get_all_media(self):
        rows = self.BDmanager.select_all("media")
        return [BaseDoc(media[0], media[2], media[1], media[4], media[5], media[6], media[3]) for media in rows]


    # Return true if chat with user exist, false if not
    # param : user_id - id of user
    # return : bool value
    def chat_exists(self, user_id):
        return any(
            [self.BDmanager.select_label('librarians', user_id), self.BDmanager.select_label('patrons', user_id)])


    # Removes a user from the database
    # param : user_id - id of user
    # param : table - the table from which you want to delete the user
    # return : bool value - True if deletion was successful, false - if not
    def remove_user(self, user_id, table=None):
        if table != None:
            if self.BDmanager.select_label(table, user_id):
                self.BDmanager.delete_label(table, user_id)
                return True
            else:
                return False
        else:
            if self.BDmanager.select_label('librarians', user_id):
                self.BDmanager.delete_label('librarians', user_id)
                return True
            elif self.BDmanager.select_label('patrons', user_id):
                self.BDmanager.delete_label('patrons', user_id)
                return True
            else:
                return False


    # Return user by id
    # param : user_id - id of user
    # return : dictionary user {id,name,address,phone,status} if user librarian or unconfirmed,
    # or {id,name,address,phone,history,current_books,status}, 
    # or false if user doesn`t exist 
    def get_user(self, user_id):
        user = {}
        if self.BDmanager.select_label('patrons', user_id):
            user_bd = self.BDmanager.select_label('patrons', user_id)
            user['id'] = user_bd[0]
            user['name'] = user_bd[1]
            user['address'] = user_bd[2]
            user['phone'] = user_bd[3]
            user['history'] = user_bd[4]
            user['current_books'] = user_bd[5]
            user['status'] = user_bd[6]
        elif self.BDmanager.select_label('librarians', user_id):
            user_bd = self.BDmanager.select_label('librarians', user_id)
            user['id'] = user_bd[0]
            user['name'] = user_bd[1]
            user['phone'] = user_bd[2]
            user['address'] = user_bd[3]
            user['status'] = user_bd[4]
        elif self.BDmanager.select_label('unconfirmed',user_id):
            user_bd = self.BDmanager.select_label('unconfirmed', user_id)
            user['id'] = user_bd[0]
            user['name'] = user_bd[1]
            user['phone'] = user_bd[2]
            user['address'] = user_bd[3]
            user['status'] = user_bd[4]
        else:
            return False
        return user


    # Move patron from table patrons to table librarians
    # param: user_id : id of user
    def upto_librarian(self, user_id):
        user_info = self.get_user(user_id)
        self.remove_user(user_id, 'patrons')
        user_info["status"] = 'Librarian'
        self.BDmanager.add_librarian(Librarian(**user_info))

    # Returns in which table the user is located
    # param : user_id - id of user
    # return : if 0 then user is unauthorized
    #          if 1 then user is unconfirmed
    #          if 2 then user is patron
    #          if 3 then user is admin
    def user_type(self, user_id):
        d = {"unauthorized": 0, 'unconfirmed': 1, 'patron': 2, 'admin': 3}
        if self.BDmanager.select_label('librarians', user_id):
            return d['admin']
        elif self.BDmanager.select_label('patrons', user_id):
            return d['patron']
        elif self.BDmanager.select_label('unconfirmed', user_id):
            return d['unconfirmed']
        else:
            return d['unauthorized']
