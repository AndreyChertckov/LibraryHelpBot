from DataBase.DBmanager import Manager
from Controller.controller import Controller
from DataBase.DBPackager import Packager

d1 = {'title': 'Introduction to Algorithms',
      'authors': 'Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein',
      'description': 'Book about OOP. MIT Press 2009.Third edition', 'count': 0, 'free_count': 0, 'price': 5000,
      'best_seller': 0,
      'keywords': 'Algorithms, OOP,programming'}

d2 = {'title': 'Algorithms + Data Structures = Programs',
      'authors': ': Niklaus Wirth',
      'description': 'Book about algorithms. 1978 First edition', 'count': 0,
      'free_count': 0, 'price': 5000,
      'best_seller': 1,
      'keywords': 'Algorithms, Data Structures, Search Algorithms, Pascal'}

d3 = {'title': 'The Art of Computer Programming',
      'authors': 'Donald E. Knuth',
      'description': 'Addison Wesley Longman Publishing Co., Inc. 1997. Third edition',
      'count': 0, 'free_count': 0, 'price': 5000,
      'best_seller': 0,
      'keywords': 'Algorithms, Combinatorial Algorithms, Recursion'}

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

l1 = {'id': 1, 'phone': 12345, 'name': 'Lib1', 'address': 'Inno', 'status': 'patron', 'privileges': 1}
l2 = {'id': 2, 'phone': 12345, 'name': 'Lib2', 'address': 'Inno', 'status': 'patron', 'privileges': 2}
l3 = {'id': 3, 'phone': 12345, 'name': 'Lib3', 'address': 'Inno', 'status': 'patron', 'privileges': 3}

c = Controller(testing=True)

m = Manager(logging=True, controller=c)


def clear_tables():
    m.drop_tables()


'''
Priv1: Access to/Modification of documents and patrons’ information.
Priv2: In addition to Priv1, addition of documents and patrons to
the library.
Priv3: In addition to Priv2, deletion of documents and patrons of
the library.
'''


def test_one():
    print('Ok')


def test_two():
    clear_tables()
    m.add_librarian(Packager(l1))
    m.add_librarian(Packager(l2))
    m.add_librarian(Packager(l3))
    assert (m.get_count('librarians') == 3)
    return True


def test_three():
    test_two()
    c.add_document(d1, 'book', l1['id'])
    c.add_document(d2, 'book', l1['id'])
    c.add_document(d3, 'book', l1['id'])

    assert (c.add_copies_of_document('book', 1, 3, l1['id']) == False)
    assert (c.add_copies_of_document('book', 2, 3, l1['id']) == False)
    assert (c.add_copies_of_document('book', 3, 3, l1['id']) == False)
    assert (m.get_count('book') == 0)
    return True


def test_four():
    test_two()
    c.add_document(d1, 'book', l2['id'])
    c.add_document(d2, 'book', l2['id'])
    c.add_document(d3, 'book', l2['id'])

    c.add_copies_of_document('book', 1, 3, by_who_id=l2['id'])
    c.add_copies_of_document('book', 2, 3, by_who_id=l2['id'])
    c.add_copies_of_document('book', 3, 3, by_who_id=l2['id'])
    m.add_patron(Packager(p1), 2)
    m.add_patron(Packager(p2), 2)
    m.add_patron(Packager(p3), 2)
    m.add_patron(Packager(s), 2)
    m.add_patron(Packager(v), 2)

    assert (m.get_count('patrons') == 5)
    return True


def test_five():
    test_four()
    c.add_copies_of_document('book', 1, -1, by_who_id=l2['id'])
    assert (m.get_label('count', 'book', 1) == 2)
    return True


def test_six():
    test_four()
    c.check_out_doc(p1['id'], 3)
    c.check_out_doc(p2['id'], 3)
    c.check_out_doc(s['id'], 3)
    c.check_out_doc(v['id'], 3)
    c.check_out_doc(p3['id'], 3)
    assert (c.outstanding_request(3, 'book', by_who_id=1) == False)
    return True


def test_seven():
    test_four()
    c.check_out_doc(p1['id'], 3)
    c.check_out_doc(p2['id'], 3)
    c.check_out_doc(s['id'], 3)
    c.check_out_doc(v['id'], 3)
    c.check_out_doc(p3['id'], 3)
    req = c.outstanding_request(3, 'book', by_who_id=3)
    assert (c.get_document_queue('book', 3) == [])
    assert (req == [[v['id'], p3['id']], [p1['id'], p2['id'], s['id']]])
    return True

def test_eight():
    test_six()
    print('Check log')

def test_nine():
    test_seven()
    print('Check log')


def test_ten():
    test_four()
    res_book = Packager(c.get_documents_by_title('Introduction to Algorithms', 'book')[0])
    assert (res_book.title == d1['title']
            and res_book.authors == d1['authors'])
    return True

def test_eleven():
    test_four()
    res = c.get_documents_by_title('Algorithms', 'book')
    assert ([i['title'] for i in res] == [d1['title'], d2['title']])
    return True

def test_twelve():
    test_four()
    res = c.get_documents_by_keywords('Algorithms', 'book')
    assert ([i['title'] for i in res] == [d1['title'], d2['title'], d3['title']])
    return True

def run_test(i):
    tests = [test_one, test_two, test_three, test_four, test_five,
             test_six, test_seven, test_eight, test_nine, test_ten, test_eleven(), test_twelve()]
    tests[i]()
    return True

i = 0

while (True):
    print('Enter test number:')
    test=int(input())
    print(run_test(i))
