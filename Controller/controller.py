from DataBase.BDmanagement import BDManagement
from DataBase.UsersAndDocumentObjects.Patron import Patron

class Controller:

	def __init__(self):
		self.BDmanager = BDManagement()

	def registration(self,user_info):
		user_info = user_info
		print(user_info)
		if user_info['status'] != "Librarian":
			patron = Patron(name=user_info['name'],address=user_info['address'],type=user_info['status'],id=user_info['id'],phone=user_info['phone number'])
			self.BDmanager.add_patron(patron)