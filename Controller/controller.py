from DataBase.BDmanagement import BDManagement
from DataBase.UsersAndDocumentObjects.Patron import Patron
from DataBase.UsersAndDocumentObjects.Librarian import Librarian

class Controller:

	def __init__(self):
		self.BDmanager = BDManagement()

	def registration(self,user_info):
		user_info = user_info
		print(user_info)
		if user_info['status'] != "Librarian":
			patron = Patron(name=user_info['name'],address=user_info['address'],
							type=user_info['status'],id=user_info['id'],phone=user_info['phone number'])
			self.BDmanager.add_patron(patron)
		else:
			librarian = Librarian(user_info['name'],user_info['address'],user_info['id'],user_info['phone'])
			self.BDmanager.add_librarian(librarian)

    def get_all_patrons(self):
        rows = self.BDmanager.select_all("patrons")
        return [Patron(x[1], x[3], "patron", x[0], x[2], x[4], x[5], 2) for x in rows]

    def get_all_librarians(self):
        rows = self.BDmanager.select_all("librarians")
        return [Librarian(x[1], x[3], x[0], x[2]) for x in rows]

    def get_all_books(self):
        rows = self.BDmanager.select_all("books")
        return [Document(x[1], x[3], x[2], x[0], x[4], x[5], x[6]) for x in rows]

    def get_all_articles(self):
        rows = self.BDmanager.select_all("articles")
        return [JournalArticle(x[1], x[2], x[3], x[4], x[0], x[5], x[6], x[7]) for x in rows]

    def get_all_media(self):
        rows = self.BDmanager.select_all("media")
        return [BaseDoc(x[0], x[2], x[1], x[4], x[5], x[6], x[3]) for x in rows]

    def get_all_chats(self):
        rows = self.BDmanager.select_all("chats")
        return [chat(x[0], x[1], x[2]) for x in rows]

    def chat_exists(self, id):
        return any(x.get_chat_id() == id for x in self.get_all_chats())