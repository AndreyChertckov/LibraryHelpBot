from Controller.controller import Controller
from DataBase.UsersAndDocumentObjects.Patron import Patron
from DataBase.UsersAndDocumentObjects.Librarian import Librarian
import os

def us1(controller):
	controller.log('INFO','USER STORY 1')
	test_user = {'id':1,'name':'test','address':'tEsT','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}

	controller.BDmanager.add_patron(Patron(**test_user))
	controller.add_document(test_book,'book')
	book_id = controller.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	controller.check_out_doc(test_user['id'],book_id,'book',2)
	controller.BDmanager.clear_table('patrons')
	controller.BDmanager.clear_table('book')

def us2(controller):
	controller.log('INFO','USER STORY 2')
	test_user = {'id':1,'name':'test','address':'tEsT','status':'Faculty','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}

	controller.BDmanager.add_patron(Patron(**test_user))
	controller.add_document(test_book,'book')
	book_id = controller.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	controller.check_out_doc(test_user['id'],book_id,'book',1)
	controller.BDmanager.clear_table('patrons')
	controller.BDmanager.clear_table('book')

def us3(controller):
	controller.log('INFO','USER STORY 3')
	
	test_user = {'id':1,'name':'s','address':'Innopolis','status':'Student','phone':'123132'}
	test_librarian = {'id':2,'name':'Test Librarian','address':'Innopolis','status':'Librarian','phone':'123132'}
	controller.BDmanager.add_librarian(Librarian(**test_librarian))
	controller.registration(test_user)
	controller.confirm_user(test_user['id'],test_librarian['id'])
	controller.BDmanager.clear_table('patrons')
	controller.BDmanager.clear_table('librarians')

def us4(controller):
	controller.log('INFO','USER STORY 4')

	test_librarian = {'id':2,'name':'Test Librarian','address':'Innopolis','status':'Librarian','phone':'123132'}
	controller.BDmanager.add_librarian(Librarian(**test_librarian))
	
	controller.get_all_patrons(test_librarian['id'])
	controller.BDmanager.clear_table('librarians')

def us5(controller):
	controller.log('INFO','USER STORY 5')

	test_librarian = {'id':2,'name':'Test Librarian','address':'Innopolis','status':'Librarian','phone':'123132'}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}
	controller.BDmanager.add_librarian(Librarian(**test_librarian))
	controller.add_document(test_book,'book',test_librarian['id'])
	test_book_id = controller.BDmanager.get_by('name','book',test_book['title'])[0][0]
	controller.modify_document({'id':test_book_id,'price':1},'book',test_librarian['id'])

	controller.BDmanager.clear_table('librarians')
	controller.BDmanager.clear_table('book')

def us6(controller):
	controller.log('INFO','USER STORY 6')

	test_librarian = {'id':2,'name':'Test Librarian','address':'Innopolis','status':'Librarian','phone':'123132'}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}
	controller.BDmanager.add_librarian(Librarian(**test_librarian))
	controller.add_document(test_book,'book',test_librarian['id'])
	test_book_id = controller.BDmanager.get_by('name','book',test_book['title'])[0][0]
	controller.modify_document({'id':test_book_id,'count':3},'book',test_librarian['id'])

	controller.BDmanager.clear_table('librarians')
	controller.BDmanager.clear_table('book')

def us7(controller):
	controller.log('INFO','USER STORY 7')

	test_librarian = {'id':2,'name':'Test Librarian','address':'Innopolis','status':'Librarian','phone':'123132'}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}
	controller.BDmanager.add_librarian(Librarian(**test_librarian))
	controller.add_document(test_book,'book',test_librarian['id'])
	controller.BDmanager.clear_table('librarians')
	controller.BDmanager.clear_table('book')

def us8(controller):
	controller.log('INFO','USER STORY 8')

	test_librarian = {'id':2,'name':'Test Librarian','address':'Innopolis','status':'Librarian','phone':'123132'}
	test_user = {'id':1,'name':'test','address':'tEsT','status':'Student','phone':'987', 'history':[],'current_books':[]}
	controller.BDmanager.add_librarian(Librarian(**test_librarian))
	controller.BDmanager.add_patron(Patron(**test_user))
	controller.modify_user(test_user['id'],{'name':'TESTER'},test_librarian['id'])
	controller.BDmanager.clear_table('librarians')
	controller.BDmanager.clear_table('patrons')

def user_story():
	try:
		controller = Controller('test.db',True,True,'user_story.log')
		us1(controller)
		us2(controller)
		us3(controller)
		us4(controller)
		us5(controller)
		us6(controller)
		us7(controller)
		us8(controller)
		# us9(controller)
		# us10(controller)
		# us11(controller)
		# us12(controller)
		# us13(controller)
		# us14(controller)
		# us15(controller)
		# us16(controller)
		# us17(controller)
		os.remove('test.db')
	except Exception as e:
		os.remove('test.db')
		raise(e)

if __name__ == '__main__':
	user_story()