from DataBase.BDmanagement import BDManagement
from DataBase.UsersAndDocumentObjects.Patron import Patron
from DataBase.UsersAndDocumentObjects.Librarian import Librarian


class Controller:
    def __init__(self):
        self.BDmanager = BDManagement()

    def registration(self, user_info):
        user_info = user_info
        if not self.chat_exists(user_info['id']):
            if user_info['status'] != "Librarian":
                patron = Patron(name=user_info['name'], address=user_info['address'], type=user_info['status'],
                                id=user_info['id'], phone=user_info['phone'])
                self.BDmanager.add_patron(patron)
            else:
                librarian = Librarian(user_info['name'], user_info['address'], user_info['id'], user_info['phone'])
                self.BDmanager.add_librarian(librarian)
        else:
            print('Chat exist in BD!')

    def delete_user(self, user_info):
        print(self.remove_user(user_info['id'], user_info['status']))

    # def get_all_patrons(self):
    #     rows = self.BDmanager.select_all("patrons")
    #     return [Patron(x[1], x[3], "patron", x[0], x[2], x[4], x[5], 2) for x in rows]

    # def get_all_librarians(self):
    #     rows = self.BDmanager.select_all("librarians")
    #     return [Librarian(x[1], x[3], x[0], x[2]) for x in rows]

    # def get_all_books(self):
    #     rows = self.BDmanager.select_all("books")
    #     return [Document(x[1], x[3], x[2], x[0], x[4], x[5], x[6]) for x in rows]

    # def get_all_articles(self):
    #     rows = self.BDmanager.select_all("articles")
    #     return [JournalArticle(x[1], x[2], x[3], x[4], x[0], x[5], x[6], x[7]) for x in rows]

    # def get_all_media(self):
    #     rows = self.BDmanager.select_all("media")
    #     return [BaseDoc(x[0], x[2], x[1], x[4], x[5], x[6], x[3]) for x in rows]

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

    def request_on_add_librarian(self,user_info):
        pass

    def generate_key(self,alias):
        pass