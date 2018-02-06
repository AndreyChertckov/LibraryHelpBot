from Controller.controller import Controller
from DataBase.BDmanagement import BDManagement


def first_test(cntrl):
	pass


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
	user_bd_t = dbmanage.select_label(table,user['id'])
	if not user_bd_t:
		return False
	
	user_bd = {'id':user_bd_t[0],'name':user_bd_t[1],'phone':user_bd_t[2],'address':user_bd_t[3]}
	if table == 'patrons':
		user_bd['address'] = user_bd_t[3]
		user_bd['phone'] = user_bd_t[2]
		user_bd['status'] = user_bd_t[6]
	elif table == 'librarians':
		user_bd['phone'] = user_bd_t[3]
		user_bd['address'] = user_bd_t[2]
		user_bd['status'] = user_bd_t[4]
	elif table == 'unconfirmed':
		user_bd['address'] = user_bd_t[3]
		user_bd['phone'] = user_bd_t[2]
		user_bd['status'] = user_bd_t[4]
	for key in user.keys():
		if user[key] != user_bd[key]:
			return False

	return True

def test_controller():
    cntrl = Controller('test.bd')
    msg,err = test_registration_confirm_uptolibrarian(cntrl)
    print("test_registration_confirm_uptolibrarian : " + msg)

if __name__ == '__main__':
    test_controller()
