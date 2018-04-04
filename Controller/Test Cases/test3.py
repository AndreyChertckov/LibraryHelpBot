import pytest
from DataBase.DBmanager import Manager
from DataBase.DBPackager import Packager
from Controller.controller import Controller
from datetime import date, datetime

'''
Name: Sergey Afonso
Address: Via Margutta, 3
Phone Number: 30001
Lib. card ID: 1010
Type: Faculty (Professor)
'''
d1 = {'title': 'Introduction to Algorithms',
      'authors': 'Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein',
      'description': 'Book about OOP. MIT Press 2009.Third edition', 'count': 10, 'free_count': 10, 'price': 5000,
      'best_seller': 0,
      'keywords': 'OOP,programming'}

d2 = {'title': 'Design Patterns: Elements of Reusable Object-Oriented Software',
      'authors': ': Erich Gamma, Ralph Johnson, John Vlissides, Richard Helm',
      'description': 'OOP as design-pattern. Addison-Wesley Professional 2003.First edition', 'count': 10,
      'free_count': 10, 'price': 1700,
      'best_seller': 1,
      'keywords': 'OOP,programming'}

d3 = {'title': 'The Mythical Man-month', 'authors': 'Brooks,Jr., Frederick P',
      'description': 'Book about software  Engineering.1995.Second edition', 'count': 2, 'free_count': 2, 'price': 700,
      'best_seller': 0,
      'keywords': ''}

p1 = {'id': 1010, 'name': 'Sergey Afonso', 'address': 'Via Margutta, 3',
      'status': 'Professor', 'phone': '30001', 'history': [], 'current_docs': []}

p2 = {'id': 1011, 'name': 'Nadia Teixeira', 'address': 'Via Sacra, 13',
      'status': 'Professor', 'phone': '30002', 'history': [], 'current_docs': []}

p3 = {'id': 1100, 'name': 'Elvira Espindola', 'address': 'Via del Corso, 22',
      'status': 'Professor', 'phone': '30003', 'history': [], 'current_docs': []}

s = {'id': 1101, 'name': 'Andrey Velo', 'address': 'Avenida Mazatlan 250',
     'status': 'Student', 'phone': ': 30004', 'history': [], 'current_docs': []}

v = {'id': 1110, 'name': 'Veronika Rama', 'address': 'Stret Atocha, 27',
     'status': 'Visiting Professor', 'phone': ': 30005', 'history': [], 'current_docs': []}

date1 = datetime(2018, 3, 5)
date2 = date(2018, 4, 2)
date3 = datetime(2018, 3, 29)
date4 = datetime(2018, 3, 26)
m = Manager()
c = Controller()

def clear_tables():
    m.drop_tables()
    add_all()
def check_out_doc(user_id, doc_id, type_bd, date=datetime.now()):
    if (c.check_out_doc(user_id, doc_id, type_bd, date_when_took=date)[0] == False):
        c.add_queue_order(user_id, type_bd, doc_id)


def return_doc(user_id, doc_id):
    orders = c.get_user_orders(user_id)
    for id in orders:
        if (id['doc_id'] == doc_id):
            c.return_doc(id['id'])


def add_all():
    m.add_patron(Packager(p1))
    m.add_patron(Packager(p2))
    m.add_patron(Packager(p3))
    m.add_patron(Packager(s))
    m.add_patron(Packager(v))
    m.add_book(Packager(d1))
    m.add_book(Packager(d2))
    m.add_book(Packager(d3))


def test_one():
    clear_tables()
    c.check_out_doc(p1['id'], 1, 'book', date_when_took=date1)
    c.check_out_doc(p1['id'], 2, 'book', date_when_took=date1)
    return_doc(p1['id'], 2)
    assert (c.calculate_fine(c.get_order(1), date_=date2) == 0
            and c.get_overdue(p1['id'], date_=date2) == [(d1['title'], 0)])
    print('OK')

def test_two():
    clear_tables()
    c.check_out_doc(p1['id'], 1, 'book', date_when_took=date1)
    c.check_out_doc(p1['id'], 2, 'book', date_when_took=date1)
    c.check_out_doc(s['id'], 1, 'book', date_when_took=date1)
    c.check_out_doc(s['id'], 2, 'book', date_when_took=date1)
    c.check_out_doc(v['id'], 1, 'book', date_when_took=date1)
    c.check_out_doc(v['id'], 2, 'book', date_when_took=date1)

    assert (c.get_overdue(p1['id'], date2) == [(d1['title'], 0), (d2['title'], 0)]
            and c.get_fine(p1['id'], date2) == [(d1['title'], 0), (d2['title'], 0)])

    assert (c.get_overdue(s['id'], date2) == [(d1['title'], 7), (d2['title'], 14)]
            and c.get_fine(s['id'], date2) == [(d1['title'], 700), (d2['title'], 1400)])

    assert (c.get_overdue(v['id'], date2) == [(d1['title'], 21), (d2['title'], 21)]
            and c.get_fine(v['id'], date2) == [(d1['title'], 2100), (d2['title'], 1700)])
    print('OK')

def test_three():
    clear_tables()
    c.check_out_doc(p1['id'], 1, 'book', date_when_took=date3)
    c.check_out_doc(s['id'], 2, 'book', date_when_took=date3)
    c.check_out_doc(v['id'], 2, 'book', date_when_took=date3)

    c.renew_item(1)
    c.renew_item(2)
    c.renew_item(3)

    assert (c.get_user_due(p1['id']) == [(d1['title'], '2018-05-03')])
    assert (c.get_user_due(s['id']) == [(d2['title'], '2018-04-19')])
    assert (c.get_user_due(v['id']) == [(d2['title'], '2018-04-12')])
    print('OK')

def test_four():
    clear_tables()
    c.check_out_doc(p1['id'], 1, 'book', date_when_took=date3)
    c.check_out_doc(s['id'], 2, 'book', date_when_took=date3)
    c.check_out_doc(v['id'], 2, 'book', date_when_took=date3)

    c.place_outstanding(2, 'book', date2)
    c.renew_item(1)
    c.renew_item(2)
    c.renew_item(3)

    assert (c.get_user_due(p1['id']) == [(d1['title'], '2018-05-03')])
    assert (c.get_user_due(s['id']) == [(d2['title'], '2018-04-02')])
    assert (c.get_user_due(v['id']) == [(d2['title'], '2018-04-02')])
    print('OK')

def test_five():
    clear_tables()
    c.check_out_doc(p1['id'], 3, 'book', date_when_took=date3)
    c.check_out_doc(s['id'], 3, 'book', date_when_took=date3)
    if (c.check_out_doc(v['id'], 3, 'book', date_when_took=date3)[0] == False):
        c.add_queue_order(v['id'], 'book', 3)
    assert (c.get_document_queue('book', 3)[0]['id'] == v['id'])
    print('OK')


def test_six():
    clear_tables()
    check_out_doc(p1['id'], 3, 'book', date=date3)
    check_out_doc(p2['id'], 3, 'book', date=date3)
    check_out_doc(s['id'], 3, 'book', date=date3)
    check_out_doc(v['id'], 3, 'book', date=date3)
    check_out_doc(p3['id'], 3, 'book', date=date3)
    assert ([i['id'] for i in c.get_document_queue('book', 3)] == [s['id'], v['id'], p3['id']])
    print('OK')

def test_seven():
    clear_tables()
    test_six()
    a = c.place_outstanding(3, 'book')
    assert (c.get_document_queue('book', 3) == [])
    assert (a[1] == [p1['id'], p2['id']])
    assert (a[0] == [s['id'], v['id'], p3['id']])
    print('OK')

def test_eight():
    clear_tables()
    test_six()
    c.return_doc(2, True)
    assert (m.get_label('current_docs', 'patrons', p2['id']) == '[]')
    assert ([i['id'] for i in c.get_document_queue('book', 3)] == [s['id'], v['id'], p3['id']])


def test_nine():
    clear_tables()
    test_six()
    c.renew_item(1)
    assert (c.get_user_due(p1['id']) == [(d3['title'], '2018-04-26')])
    assert ([i['id'] for i in c.get_document_queue('book', 3)] == [s['id'], v['id'], p3['id']])
    print('OK')

def test_ten():
    clear_tables()
    check_out_doc(p1['id'], 1, 'book', date=date4)
    c.renew_item(1)
    check_out_doc(v['id'], 1, 'book', date=date4)
    c.renew_item(2)
    c.renew_item(1)
    c.renew_item(2)
    assert (c.get_user_due(p1['id']) == [(d1['title'], '2018-04-30')])
    assert (c.get_user_due(v['id']) == [(d1['title'], '2018-04-16')])
    print('OK')

def test_all():
    for i in range(1,10):
        run_test(i)

def run_test(i):
    tests=[test_one,test_two,test_three,test_four,test_five,
           test_six,test_seven,test_eight,test_nine,test_ten]
    tests[i]()

# test_all()