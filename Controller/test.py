import os

from Controller.controller import Controller
from DataBase.BDmanagement import BDManagement
from DataBase.UsersAndDocumentObjects.Patron import Patron

def first_test(cntrl):
	
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':2}
	test_book = {'name': 'Test','description':'TESTTEST','author':'tEsT','count':2,'price':123}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)


def test_add_book(cntrl):
	
	test_book_1 = {'name': 'Test','description':'TESTTEST','author':'tEsT','count':2,'price':123}
	test_book_2 = {'name': 'Test2','description':'TESTTEST2','author':'tEsT2','count':1,'price':1223}
	
	cntrl.add_book(**test_book_1)
	cntrl.add_book(**test_book_2)

	is_in_db_first_book = check_in_db_books(cntrl.BDmanager,test_book_1)
	is_in_db_second_book = check_in_db_books(cntrl.BDmanager,test_book_2)
	if not is_in_db_first_book or not is_in_db_second_book:
		return 'Can`t add book in db. First book added: ' + is_in_db_first_book + ' , Second book added : ' + is_in_db_second_book,False

	return 'OK',True


def test_registration_confirm_uptolibrarian(cntrl):
	
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987'}
	cntrl.registration(test_user)
	if not check_in_db_users(cntrl.BDmanager,'unconfirmed',test_user):
		return 'Can`t registrate',False
	
	cntrl.confirm_user(test_user['id'])
	in_unconfirmed_table = check_in_db_users(cntrl.BDmanager,'unconfirmed',test_user)
	in_patrons_table = check_in_db_users(cntrl.BDmanager,'patrons',test_user)
	if  in_unconfirmed_table or not in_patrons_table:
		return 'Can`t confirm user, in unconfirmed table: ' + str(in_unconfirmed_table) + ', in patrons table: ' + str(in_patrons_table),False

	cntrl.upto_librarian(test_user['id'])
	test_user['status'] = 'librarian'
	if check_in_db_users(cntrl.BDmanager,'patrons',test_user) or not check_in_db_users(cntrl.BDmanager,'librarians',test_user):
		return 'Can`t up to librarian',False

	cntrl.remove_user(test_user['id'],'librarians')

	return 'OK',True


def check_in_db_users(dbmanage,table,user):
	user_db_t = dbmanage.select_label(table,user['id'])
	if not user_db_t:
		return False
	
	user_db = {'id':user_db_t[0],'name':user_db_t[1],'phone':user_db_t[2],'address':user_db_t[3]}
	if table == 'patrons':
		user_db['address'] = user_db_t[3]
		user_db['phone'] = user_db_t[2]
		user_db['status'] = user_db_t[6]
	elif table == 'librarians':
		user_db['phone'] = user_db_t[3]
		user_db['address'] = user_db_t[2]
		user_db['status'] = user_db_t[4]
	elif table == 'unconfirmed':
		user_db['address'] = user_db_t[3]
		user_db['phone'] = user_db_t[2]
		user_db['status'] = user_db_t[4]
	for key in user.keys():
		if user[key] != user_db[key]:
			return False

	return True


def check_in_db_books(dbmanage,book):
	book_db_t = list(dbmanage.get_by('name','books',book['name'])[0])
	book_db = dict(zip(['id','name','author','description','count','free_count','price'],book_db_t))
	for key in book.keys():
		if book[key] != book_db[key]:
			return False
	return True


def test_controller():
    cntrl = Controller('test.db')
    msg,err = test_registration_confirm_uptolibrarian(cntrl)
    print("test_registration_confirm_uptolibrarian : " + msg)
    msg,err = test_add_book(cntrl)
    print('test_add_book : ' + msg)
    os.remove('test.db')

if __name__ == '__main__':
    test_controller()
