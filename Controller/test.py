import os
from datetime import datetime
from datetime import timedelta

from Controller.controller import Controller
from DataBase.BDmanagement import BDManagement
from DataBase.UsersAndDocumentObjects.Patron import Patron

def test_first():

	cntrl = create_controller(1)

	test_user = {'id':1,'name':'test','address':'tEsT','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	cntrl.check_out_doc(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','book',test_book['title'])[0])
	book_db = dict(zip(['id','title','authors','overview','count','free_count','price'],book_db_t))
	order_id = int(eval(user_db['current_docs'])[0])
	user_book_id = cntrl.BDmanager.get_by('id','orders',order_id)[0][3]

	is_user_have_book = user_book_id == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	clear_tables()
	assert(is_book_free_count_decremented and is_user_have_book)


def test_second():
	
	cntrl = create_controller(2)

	id_book_A = 1
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	cntrl.BDmanager.add_patron(Patron(**test_user))
	can_get_book = cntrl.check_out_doc(test_user['id'],id_book_A)
	clear_tables()
	assert(can_get_book)


def test_third():

	cntrl = create_controller(3)

	test_user = {'id':1,'name':'test','address':'test','status':'Faculty','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	cntrl.check_out_doc(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','book',test_book['title'])[0])
	book_db = dict(zip(['id','title','authors','overview','count','free_count','price','keywords'],book_db_t))
	order_id = int(eval(user_db['current_docs'])[0])
	order = dict(zip(['id','time','table','userId','docId','out_of_time'],list(cntrl.BDmanager.get_by('id','orders',order_id)[0])))

	order['time'] = datetime.strptime(order['time'],'%Y-%m-%d')
	order['out_of_time'] = datetime.strptime(order['out_of_time'],'%Y-%m-%d')

	is_user_have_book = order['docId'] == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	is_out_of_time_equality = order['out_of_time'] == order['time'] + timedelta(weeks = 4)
	clear_tables()
	assert(is_user_have_book and is_book_free_count_decremented and is_out_of_time_equality)

def test_fourth():
	
	cntrl = create_controller(4)

	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'best_seller':1,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	cntrl.check_out_doc(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','book',test_book['title'])[0])
	book_db = dict(zip(['id','title','authors','overview','count','free_count','price','keywords'],book_db_t))
	order_id = int(eval(user_db['current_docs'])[0])
	order = dict(zip(['id','time','table','userId','docId','out_of_time'],list(cntrl.BDmanager.get_by('id','orders',order_id)[0])))
	
	order['time'] = datetime.strptime(order['time'],'%Y-%m-%d')
	order['out_of_time'] = datetime.strptime(order['out_of_time'],'%Y-%m-%d') 

	is_user_have_book = order['docId'] == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	is_out_of_time_equality = order['out_of_time'] == order['time'] + timedelta(weeks = 2)
	clear_tables()
	assert(is_user_have_book and is_book_free_count_decremented and is_out_of_time_equality)


def test_fifth():

	cntrl = create_controller(5)
	
	test_user_1 = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_user_2 = {'id':2,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_user_3 = {'id':3,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}

	cntrl.BDmanager.add_patron(Patron(**test_user_1))
	cntrl.BDmanager.add_patron(Patron(**test_user_2))
	cntrl.BDmanager.add_patron(Patron(**test_user_3))

	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}
	
	cntrl.add_book(**test_book)

	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	is_first_user_check_out = cntrl.check_out_doc(test_user_1['id'],book_id)
	is_second_user_check_out = cntrl.check_out_doc(test_user_3['id'],book_id)
	is_third_user_check_out = cntrl.check_out_doc(test_user_2['id'],book_id)
	clear_tables()
	assert(is_first_user_check_out[0] and is_second_user_check_out[0] and not is_third_user_check_out[0])


def test_sixth():

	cntrl = create_controller(6)
	
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	first_copy = cntrl.check_out_doc(test_user['id'],book_id)[0]
	second_copy = cntrl.check_out_doc(test_user['id'],book_id)[0]
	clear_tables()
	assert(first_copy and not second_copy)

def test_seventh():

	cntrl = create_controller(7)

	test_user_1 = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_user_2 = {'id':2,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}

	cntrl.BDmanager.add_patron(Patron(**test_user_1))
	cntrl.BDmanager.add_patron(Patron(**test_user_2))

	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}
	
	cntrl.add_book(**test_book)

	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	is_first_user_check_out = cntrl.check_out_doc(test_user_1['id'],book_id)
	is_second_user_check_out = cntrl.check_out_doc(test_user_2['id'],book_id)
	clear_tables()
	assert(is_first_user_check_out[0] and is_second_user_check_out[0])


def test_eighth():

	cntrl = create_controller(8)
	
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	cntrl.check_out_doc(test_user['id'],book_id,'book',3)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','book',test_book['title'])[0])
	book_db = dict(zip(['id','title','author','overview','count','free_count','price','keywords'],book_db_t))
	order_id = int(eval(user_db['current_docs'])[0])
	order = dict(zip(['id','time','table','userId','docId','out_of_time'],list(cntrl.BDmanager.get_by('id','orders',order_id)[0])))
	
	order['time'] = datetime.strptime(order['time'],'%Y-%m-%d')
	order['out_of_time'] = datetime.strptime(order['out_of_time'],'%Y-%m-%d')

	is_user_have_book = order['docId'] == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	is_out_of_time_equality = order['out_of_time'] == order['time'] + timedelta(weeks = 3)
	clear_tables()
	assert( is_user_have_book and is_book_free_count_decremented and is_out_of_time_equality)


def test_ninth():
	
	cntrl = create_controller(9)

	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	cntrl.check_out_doc(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','book',test_book['title'])[0])
	book_db = dict(zip(['id','title','authors','overview','count','free_count','price','keywords'],book_db_t))
	order_id = int(eval(user_db['current_docs'])[0])
	order = dict(zip(['id','time','table','userId','docId','out_of_time'],list(cntrl.BDmanager.get_by('id','orders',order_id)[0])))
	
	order['time'] = datetime.strptime(order['time'],'%Y-%m-%d')
	order['out_of_time'] = datetime.strptime(order['out_of_time'],'%Y-%m-%d') 

	is_user_have_book = order['docId'] == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	is_out_of_time_equality = order['out_of_time'] == order['time'] + timedelta(weeks = 2)
	clear_tables()
	assert(is_user_have_book and is_book_free_count_decremented and is_out_of_time_equality)


def test_tenth():

	cntrl = create_controller(10)

	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book_1 = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}
	test_book_2 = {'title': 'TEEST','overview':'TESTTEST','authors':'tEsT','count':0,'price':122,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	
	cntrl.add_book(**test_book_1)
	cntrl.add_book(**test_book_2)

	book_id_1 = cntrl.BDmanager.get_by('name','book',test_book_1['title'])[0][0]
	book_id_2 = cntrl.BDmanager.get_by('name','book',test_book_2['title'])[0][0]

	regular_book = cntrl.check_out_doc(test_user['id'],book_id_1)[0]
	references_book = not cntrl.check_out_doc(test_user['id'],book_id_2)[0]
	clear_tables()
	assert( regular_book and references_book)

def test_add_book():

	cntrl = create_controller('test_add_book')
	
	test_book_1 = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':0}
	test_book_2 = {'title': 'Test2','overview':'TESTTEST2','authors':'tEsT2','count':1,'price':1223,'keywords':0}
	
	cntrl.add_book(**test_book_1)
	cntrl.add_book(**test_book_2)

	is_in_db_first_book = check_in_db_books(cntrl.BDmanager,test_book_1)
	is_in_db_second_book = check_in_db_books(cntrl.BDmanager,test_book_2)
	clear_tables()
	assert(is_in_db_first_book and is_in_db_second_book)

def test_registration_confirm_uptolibrarian():
	
	cntrl = create_controller('test_registration_confirm_uptolibrarian')

	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987'}
	cntrl.registration(test_user)
	if not check_in_db_users(cntrl.BDmanager,'unconfirmed',test_user):
		clear_tables()
		assert( False )
	
	cntrl.confirm_user(test_user['id'])
	in_unconfirmed_table = check_in_db_users(cntrl.BDmanager,'unconfirmed',test_user)
	in_patrons_table = check_in_db_users(cntrl.BDmanager,'patrons',test_user)
	if  in_unconfirmed_table or not in_patrons_table:
		clear_tables()
		assert(False)

	cntrl.upto_librarian(test_user['id'])
	test_user['status'] = 'librarian'
	if check_in_db_users(cntrl.BDmanager,'patrons',test_user) or not check_in_db_users(cntrl.BDmanager,'librarians',test_user):
		clear_tables()
		assert(False)

	clear_tables()
	assert(True)


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
	book_db_t = list(dbmanage.get_by('name','book',book['title'])[0])
	book_db = dict(zip(['id','title','authors','overview','count','free_count','price','keywords'],book_db_t))
	for key in book.keys():
		if book[key] != book_db[key]:
			print(key + " : " + str(book[key]) + ' != ' + str(book_db[key]))
			return False
	return True


def test_get_all_books():

	cntrl = create_controller('test_get_all_books')
	
	test_book_1 = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':0}
	test_book_2 = {'title': 'Test2','overview':'TESTTEST2','authors':'tEsT2','count':1,'price':1223,'keywords':0}
	
	cntrl.add_book(**test_book_1)
	cntrl.add_book(**test_book_2)

	books = cntrl.get_all_books()
	first_book = test_book_1['title'] == books[0]['title']
	second_book = test_book_2['title'] == books[1]['title']

	clear_tables()
	assert (first_book and second_book)


def test_check_out_media():

	cntrl = create_controller('test_check_out_media')
	
	test_media = {'title':'Teste','authors':'XY','keywords':'oansedi','price':123,'best_seller':1,'count':1}
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}

	cntrl.add_media(**test_media)
	cntrl.BDmanager.add_patron(Patron(**test_user))

	media_id = cntrl.BDmanager.get_by('name','media',test_media['title'])
	
	if media_id == None:
		clear_tables()
		assert(False)
	media_id = media_id[0][0]
	success,msg = cntrl.check_out_doc(test_user['id'],media_id,'media')
	if not success:
		clear_tables()
		assert(False)

	test_user = cntrl.get_user(test_user['id'])
	order = cntrl.BDmanager.select_label('orders',eval(test_user['current_docs'])[0])
	is_order_media = order[2] == 'media'
	is_ids_match = order[3] == media_id
	
	clear_tables()
	assert(is_order_media and is_ids_match)

def test_modify_doc():

	cntrl = create_controller('test_modify_doc')

	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':0}
	cntrl.add_book(**test_book)

	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	if book_id == None:
		clear_tables()
		assert(False)
	changes = {'id':book_id,'price':246,'author':'TTTTTTT'}
	cntrl.modify_document(changes,'book')
	try:
		price = cntrl.BDmanager.get_label('price','book',book_id)
		authors = cntrl.BDmanager.get_label('author','book',book_id)
		if price != changes['price'] or authors != changes['author']:
			clear_tables()
			assert(False)
		
		clear_tables()
		assert(True)
	except Exception:
		clear_tables()
		assert( False)


def test_return_doc():
	
	cntrl = create_controller('test_return_doc')

	test_media = {'title':'Teste','authors':'XY','keywords':'oansedi','price':123,'best_seller':1,'count':1}
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_media(**test_media)

	media_id = cntrl.BDmanager.get_by('name','media',test_media['title'])[0][0]

	if type(media_id) != type(1):
		clear_tables()
		assert(False)

	success,msg = cntrl.check_out_doc(test_user['id'],media_id,'media')
	
	if not success:
		clear_tables()
		assert(False)
	
	success, msg = cntrl.return_doc(test_user['id'],media_id)

	if not success:
		clear_tables()
		assert(False)
	
	user_current_docs = eval(cntrl.BDmanager.get_label('current_books','patrons',test_user['id']))
	media_count = cntrl.BDmanager.get_label('free_count','media',media_id)
	clear_currents_doc = user_current_docs == []
	count_of_media = media_count == test_media['count']
	clear_tables()
	assert(clear_currents_doc and count_of_media)


def test_delete_doc():
	
	cntrl = create_controller('test_delete_doc')

	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':0}

	cntrl.add_book(**test_book)

	doc_db = cntrl.BDmanager.get_by('name','book',test_book['title'])
	
	is_save_in_db =  doc_db != None
	doc_id = doc_db[0][0]

	cntrl.delete_document(doc_id,'book')
	doc_db = cntrl.BDmanager.select_label('book',doc_id)
	is_deleted_from_db = doc_db == None
	clear_tables()
	assert(is_deleted_from_db)

def test_get_user_orders():
	
	cntrl = create_controller('get_user_orders')

	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':'0'}
	test_user = {'id':1,'name':'test','address':'tEsT','status':'Student','phone':'987', 'history':[],'current_books':[]}

	cntrl.add_book(**test_book)
	cntrl.BDmanager.add_patron(Patron(**test_user))

	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]

	success,_ = cntrl.check_out_doc(test_user['id'],book_id)
	if not success:
		assert(success)
	
	doc = cntrl.get_user_orders(test_user['id'])[0]['doc_dict']
	clear_tables()
	assert(min([test_book[key] == doc[key] for key in test_book.keys()]))

def test_get_orders():
	
	cntrl = create_controller('get_orders')

	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':'0'}
	test_user = {'id':1,'name':'test','address':'tEsT','status':'Student','phone':'987', 'history':[],'current_books':[]}

	cntrl.add_book(**test_book)
	cntrl.BDmanager.add_patron(Patron(**test_user))

	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]

	success,_ = cntrl.check_out_doc(test_user['id'],book_id)
	if not success:
		clear_tables()
		assert(success)
	
	orders = cntrl.get_all_whaiting_doc(-1)
	if len(orders) != 1:
		clear_tables()
		assert(False)
	
	cntrl.user_get_doc(orders[0]['id'])
	orders = cntrl.get_all_active_orders(-1)
	if len(orders) != 1:
		clear_tables()
		assert(False)
	
	cntrl.return_doc(orders[0]['id'],book_id)
	orders = cntrl.get_all_returned_orders(-1)
	if len(orders) != 1:
		clear_tables()
		assert(False)
	clear_tables()
	assert(True)

def clear_tables():
	os.remove('test.db')

def create_controller(name_test):
	return Controller('test.db',False,True,'test.log',True,name_test=str(name_test))

if __name__ == '__main__':
	main()