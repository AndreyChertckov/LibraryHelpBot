import os
from datetime import datetime
from datetime import timedelta

from Controller.controller import Controller
from DataBase.BDmanagement import BDManagement
from DataBase.UsersAndDocumentObjects.Patron import Patron

def first_test(cntrl):
	
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':2}
	test_book = {'name': 'Test','description':'TESTTEST','author':'tEsT','count':2,'price':123}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','books',test_book['name'])[0][0]
	
	cntrl.check_out_book(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','books',test_book['name'])[0])
	book_db = dict(zip(['id','name','author','description','count','free_count','price'],book_db_t))
	order_id = int(eval(user_db['current_books'])[0])
	user_book_id = cntrl.BDmanager.get_by('id','orders',order_id)[0][3]

	cntrl.BDmanager.clear_table('books')
	cntrl.BDmanager.clear_table('patrons')
	cntrl.BDmanager.clear_table('orders')

	is_user_have_book = user_book_id == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	if  not is_user_have_book or not is_book_free_count_decremented:
		return 'Can`t check out book, is user have book: ' + str(is_user_have_book) + ' , is book free count decremented: ' + str(is_book_free_count_decremented), False

	return 'OK', True


def second_test(cntrl):
	
	book_db_t = cntrl.BDmanager.get_by('author','books', 'A')
	if book_db_t != []:
		return 'Book found', False

	return 'OK', True


def third_test(cntrl):
	
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':4}
	test_book = {'name': 'Test','description':'TESTTEST','author':'tEsT','count':2,'price':123}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','books',test_book['name'])[0][0]
	
	cntrl.check_out_book(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','books',test_book['name'])[0])
	book_db = dict(zip(['id','name','author','description','count','free_count','price'],book_db_t))
	order_id = int(eval(user_db['current_books'])[0])
	order = dict(zip(['id','time','table','userId','docId'],list(cntrl.BDmanager.get_by('id','orders',order_id)[0])))
	
	order['time'] = datetime.strptime(order['time'][:order['time'].index(' ')],'%Y-%m-%d')
	order['out_of_time'] = order['time'] + timedelta(weeks = test_user['check_out_time']) 

	cntrl.BDmanager.clear_table('books')
	cntrl.BDmanager.clear_table('patrons')
	cntrl.BDmanager.clear_table('orders')

	is_user_have_book = order['docId'] == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	is_out_of_time_equality = order['out_of_time'] == order['time'] + timedelta(weeks = test_user['check_out_time'])
	if  not is_user_have_book or not is_book_free_count_decremented:
		return 'Can`t check out book, is user have book: ' + str(is_user_have_book) + ' , is book free count decremented: ' + str(is_book_free_count_decremented), False

	return 'OK', True


def fourth_test(cntrl): # need best seller field in book table
	
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':4}
	test_book = {'name': 'Test','description':'TESTTEST','author':'tEsT','count':2,'price':123}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','books',test_book['name'])[0][0]
	
	cntrl.check_out_book(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','books',test_book['name'])[0])
	book_db = dict(zip(['id','name','author','description','count','free_count','price'],book_db_t))
	order_id = int(eval(user_db['current_books'])[0])
	order = dict(zip(['id','time','table','userId','docId'],list(cntrl.BDmanager.get_by('id','orders',order_id)[0])))
	
	order['time'] = datetime.strptime(order['time'][:order['time'].index(' ')],'%Y-%m-%d')
	order['out_of_time'] = order['time'] + timedelta(weeks = test_user['check_out_time']) 

	cntrl.BDmanager.clear_table('books')
	cntrl.BDmanager.clear_table('patrons')
	cntrl.BDmanager.clear_table('orders')

	is_user_have_book = order['docId'] == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	is_out_of_time_equality = order['out_of_time'] == order['time'] + timedelta(weeks = test_user['check_out_time'])
	if  not is_user_have_book or not is_book_free_count_decremented:
		return 'Can`t check out book, is user have book: ' + str(is_user_have_book) + ' , is book free count decremented: ' + str(is_book_free_count_decremented) + ', is out of time equality : ' +str(is_out_of_time_equality) , False

	return 'OK', True


def fifth_test(cntrl):
	
	test_user_1 = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':2}
	test_user_2 = {'id':2,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':2}
	test_user_3 = {'id':3,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':2}

	cntrl.BDmanager.add_patron(Patron(**test_user_1))
	cntrl.BDmanager.add_patron(Patron(**test_user_2))
	cntrl.BDmanager.add_patron(Patron(**test_user_3))

	test_book = {'name': 'Test','description':'TESTTEST','author':'tEsT','count':2,'price':123}
	
	cntrl.add_book(**test_book)

	book_id = cntrl.BDmanager.get_by('name','books',test_book['name'])[0][0]
	
	is_first_user_check_out = cntrl.check_out_book(test_user_1['id'],book_id)
	is_second_user_check_out = cntrl.check_out_book(test_user_3['id'],book_id)
	is_third_user_check_out = cntrl.check_out_book(test_user_2['id'],book_id)

	cntrl.BDmanager.clear_table('books')
	cntrl.BDmanager.clear_table('patrons')
	cntrl.BDmanager.clear_table('orders')

	
	if not is_first_user_check_out or not is_second_user_check_out or is_third_user_check_out:
		return 'Is first user check out : ' + str(is_first_user_check_out) + ', is second user check out : ' + str(is_second_user_check_out) \
			+ ', is third user check out : '+ str(is_third_user_check_out), False

	return 'OK',True


def sixth_test(cntrl):
	
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':4}
	test_book = {'name': 'Test','description':'TESTTEST','author':'tEsT','count':2,'price':123}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','books',test_book['name'])[0][0]
	
	first_copy = cntrl.check_out_book(test_user['id'],book_id)
	second_copy = cntrl.check_out_book(test_user['id'],book_id)

	cntrl.BDmanager.clear_table('books')
	cntrl.BDmanager.clear_table('patrons')
	cntrl.BDmanager.clear_table('orders')

	if not first_copy or second_copy:
		return 'Can get two copies of book. First copy : ' + str(first_copy) + ', second copy : ' + str(second_copy), False

	return 'OK', True


def seventh_test(cntrl):
	
	test_user_1 = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':2}
	test_user_2 = {'id':2,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':2}

	cntrl.BDmanager.add_patron(Patron(**test_user_1))
	cntrl.BDmanager.add_patron(Patron(**test_user_2))

	test_book = {'name': 'Test','description':'TESTTEST','author':'tEsT','count':2,'price':123}
	
	cntrl.add_book(**test_book)

	book_id = cntrl.BDmanager.get_by('name','books',test_book['name'])[0][0]
	
	is_first_user_check_out = cntrl.check_out_book(test_user_1['id'],book_id)
	is_second_user_check_out = cntrl.check_out_book(test_user_2['id'],book_id)

	cntrl.BDmanager.clear_table('books')
	cntrl.BDmanager.clear_table('patrons')
	cntrl.BDmanager.clear_table('orders')

	
	if not is_first_user_check_out or not is_second_user_check_out:
		return 'Is first user check out : ' + str(is_first_user_check_out) + ', is second user check out : ' + str(is_second_user_check_out) \
			+ ', is third user check out : '+ str(is_third_user_check_out), False

	return 'OK',True


def eighth_test(cntrl):
	
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':3}
	test_book = {'name': 'Test','description':'TESTTEST','author':'tEsT','count':2,'price':123}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','books',test_book['name'])[0][0]
	
	cntrl.check_out_book(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','books',test_book['name'])[0])
	book_db = dict(zip(['id','name','author','description','count','free_count','price'],book_db_t))
	order_id = int(eval(user_db['current_books'])[0])
	order = dict(zip(['id','time','table','userId','docId'],list(cntrl.BDmanager.get_by('id','orders',order_id)[0])))
	
	order['time'] = datetime.strptime(order['time'][:order['time'].index(' ')],'%Y-%m-%d')
	order['out_of_time'] = order['time'] + timedelta(weeks = test_user['check_out_time']) 

	cntrl.BDmanager.clear_table('books')
	cntrl.BDmanager.clear_table('patrons')
	cntrl.BDmanager.clear_table('orders')

	is_user_have_book = order['docId'] == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	is_out_of_time_equality = order['out_of_time'] == order['time'] + timedelta(weeks = test_user['check_out_time'])
	if  not is_user_have_book or not is_book_free_count_decremented:
		return 'Can`t check out book, is user have book: ' + str(is_user_have_book) + ' , is book free count decremented: ' + str(is_book_free_count_decremented) + ', is out of time equality : ' +str(is_out_of_time_equality) , False

	return 'OK', True


def ninth_test(cntrl):
		
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':2}
	test_book = {'name': 'Test','description':'TESTTEST','author':'tEsT','count':2,'price':123}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','books',test_book['name'])[0][0]
	
	cntrl.check_out_book(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','books',test_book['name'])[0])
	book_db = dict(zip(['id','name','author','description','count','free_count','price'],book_db_t))
	order_id = int(eval(user_db['current_books'])[0])
	order = dict(zip(['id','time','table','userId','docId'],list(cntrl.BDmanager.get_by('id','orders',order_id)[0])))
	
	order['time'] = datetime.strptime(order['time'][:order['time'].index(' ')],'%Y-%m-%d')
	order['out_of_time'] = order['time'] + timedelta(weeks = test_user['check_out_time']) 

	cntrl.BDmanager.clear_table('books')
	cntrl.BDmanager.clear_table('patrons')
	cntrl.BDmanager.clear_table('orders')

	is_user_have_book = order['docId'] == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	is_out_of_time_equality = order['out_of_time'] == order['time'] + timedelta(weeks = test_user['check_out_time'])
	if  not is_user_have_book or not is_book_free_count_decremented:
		return 'Can`t check out book, is user have book: ' + str(is_user_have_book) + ' , is book free count decremented: ' + str(is_book_free_count_decremented) + ', is out of time equality : ' +str(is_out_of_time_equality) , False

	return 'OK', True


def tenth_test(cntrl):

	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[],'check_out_time':2}
	test_book_1 = {'name': 'Test','description':'TESTTEST','author':'tEsT','count':2,'price':123}
	test_book_2 = {'name': 'TEEST','description':'TESTTEST','author':'tEsT','count':0,'price':122}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	
	cntrl.add_book(**test_book_1)
	cntrl.add_book(**test_book_2)

	book_id_1 = cntrl.BDmanager.get_by('name','books',test_book_1['name'])[0][0]
	book_id_2 = cntrl.BDmanager.get_by('name','books',test_book_2['name'])[0][0]

	regular_book = cntrl.check_out_book(test_user['id'],book_id_1)
	references_book = cntrl.check_out_book(test_user['id'],book_id_2)

	cntrl.BDmanager.clear_table('books')
	cntrl.BDmanager.clear_table('patrons')
	cntrl.BDmanager.clear_table('orders')

	if  not regular_book or references_book:
		return 'Regular book : ' + str(regular_book) + ' , references book : ' + str(references_book), False

	return 'OK', True


def test_add_book(cntrl):
	
	test_book_1 = {'name': 'Test','description':'TESTTEST','author':'tEsT','count':2,'price':123}
	test_book_2 = {'name': 'Test2','description':'TESTTEST2','author':'tEsT2','count':1,'price':1223}
	
	cntrl.add_book(**test_book_1)
	cntrl.add_book(**test_book_2)

	is_in_db_first_book = check_in_db_books(cntrl.BDmanager,test_book_1)
	is_in_db_second_book = check_in_db_books(cntrl.BDmanager,test_book_2)
	if not is_in_db_first_book or not is_in_db_second_book:
		return 'Can`t add book in db. First book added: ' + str(is_in_db_first_book) + ' , Second book added : ' + str(is_in_db_second_book),False

	cntrl.BDmanager.clear_table('books')

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

	cntrl.BDmanager.clear_table('patrons')

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

	msg,err = first_test(cntrl)
	print('First test : ' + msg)

	msg,err = second_test(cntrl)
	print('Second test : ' + msg)

	msg,err = third_test(cntrl)
	print('Third test : ' + msg)

	msg,err = fourth_test(cntrl)
	print('Fourth test : ' + msg)  

	msg,err = fifth_test(cntrl)
	print('Fifth test : ' + msg)

	msg,err = sixth_test(cntrl)
	print('Sixth test : ' + msg)
	
	msg,err = seventh_test(cntrl)
	print('Seventh test : ' + msg)

	msg,err = eighth_test(cntrl)
	print('Eighth test : ' + msg)
	
	msg,err = ninth_test(cntrl)
	print('Ninth test : ' + msg)
	
	msg,err = tenth_test(cntrl)
	print('Tenth test : ' + msg)

	os.remove('test.db')

if __name__ == '__main__':
	test_controller()
