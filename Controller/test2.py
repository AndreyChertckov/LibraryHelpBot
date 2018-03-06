from DataBase.DBmanager import Manager
from Controller.controller import Controller
from DataBase.DBPackager import Packager
from datetime import datetime, timedelta

c = Controller()
d = Manager()

b1 = {'title': 'Introduction to Algorithms',
      'authors': 'Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein',
      'description': 'Book about OOP. MIT Press 2009.Third edition', 'count': 0, 'free_count': 0, 'price': 1000,
      'best_seller': 0,
      'keywords': 'OOP,programming'}

b2 = {'title': 'Design Patterns: Elements of Reusable Object-Oriented Software',
      'authors': ': Erich Gamma, Ralph Johnson, John Vlissides, Richard Helm',
      'description': 'OOP as design-pattern. Addison-Wesley Professional 2003.First edition', 'count': 0,
      'free_count': 0, 'price': 1000,
      'best_seller': 1,
      'keywords': 'OOP,programming'}

b3 = {'title': 'The Mythical Man-month', 'authors': 'Brooks,Jr., Frederick P',
      'description': 'Book about software  Engineering.1995.Second edition', 'count': 0, 'free_count': 0, 'price': 1000,
      'best_seller': 0,
      'keywords': ''}

av1 = {'title': 'Null References: The Billion Dollar Mistake', 'authors': 'Tony Hoare',
       'count': 0, 'free_count': 0, 'price': 1000, 'best_seller': 0,
       'keywords': 'Null reference'}

av2 = {'title': ' Information Entropy', 'authors': 'Claude Shannon',
       'count': 0, 'free_count': 0, 'price': 1000, 'best_seller': 0,
       'keywords': 'Information'}

p1 = {'id': 1010, 'name': 'Sergey Afonso', 'address': 'Via Margutta, 3',
      'status': 'Faculty', 'phone': '30001', 'history': [], 'current_docs': []}

p2 = {'id': 1011, 'name': 'Nadia Teixeira', 'address': 'Via Sacra, 13',
      'status': 'Student', 'phone': '30002', 'history': [], 'current_docs': []}

p3 = {'id': 1100, 'name': 'Elvira Espindola', 'address': 'Via del Corso, 22',
      'status': 'Student', 'phone': '30003', 'history': [], 'current_docs': []}


def p1_is_correct(p1_):
    return p1_['name'] == 'Sergey Afonso' and p1_['address'] == 'Via Margutta, 3' and p1_['phone'] == '30001' \
           and p1_['id'] == 1010 and p1_['status'] == 'Faculty'


def p2_is_correct(p2_):
    return p2_['name'] == 'Nadia Teixeira' and p2_['address'] == 'Via Sacra, 13' and p2_['phone'] == '30002' \
           and p2_['id'] == 1011 and p2_['status'] == 'Student'


def p3_is_correct(p3_):
    return p3_['name'] == 'Elvira Espindola' and p3_['address'] == 'Via del Corso, 22' and p3_['phone'] == '30003' and \
           p3_['id'] == 1100 and p3_['status'] == 'Student'


def print_patron_info(p):
    a = [c.get_order(i) for i in eval(p['current_docs'])]
    p['current_docs'] = [(d.get_by('id', i['table'],
                                   i['doc_id'])[0][1], i['time_out']) for i in a]

    for i in p.keys():
        if (i != 'history'):
            print(i, p[i], sep=': ')
    print('==============')


def add_document(doc, type, count, id):
    c.add_document(doc, type)
    c.add_copies_of_document(type, id, count)


def clear_tables():
    d.clear_table('book')
    d.clear_table('media')
    d.clear_table('patrons')
    d.clear_table('orders')


def get_count_of_docs():
    return d.get_connection().execute("SELECT sum(count) from book").fetchone()[0] \
           + d.get_connection().execute("SELECT sum(count) from media").fetchone()[0]


def get_count_of_users():
    return d.get_count("patrons") + d.get_count("librarians")


def check_overdue(patron):
    a = [c.get_order(i) for i in eval(patron['current_docs'])]
    res = []
    for i in a:
        l = datetime.now() - datetime.strptime(i['time_out'].replace('-', ' '), '%Y %m %d')
        if (l.days > 0):
            res += [(d.get_by('id', i['table'],
                              i['doc_id'])[0][1], l.days)]
    return res


def test_one(info=False):
    clear_tables()
    add_document(b1, 'book', 3, 1)
    add_document(b2, 'book', 2, 2)
    add_document(b3, 'book', 1, 3)
    add_document(av1, 'media', 1, 1)
    add_document(av2, 'media', 1, 2)
    d.add_patron(Packager(p1))
    d.add_patron(Packager(p2))
    d.add_patron(Packager(p3))

    try:
        count_of_docs = get_count_of_docs()
        count_of_users = get_count_of_users()
        assert (count_of_docs == 8 and count_of_users == 4)
        return True
    except:
        return False


def test_two(info=False):
    test_one()
    c.add_copies_of_document('book', 1, -2)
    c.add_copies_of_document('book', 3, -1)
    d.delete_label("patrons", p2['id'])
    try:
        count_of_docs = get_count_of_docs()
        count_of_users = get_count_of_users()
        assert (count_of_docs == 5 and count_of_users == 3)
        return True
    except:
        return False


def test_three(info=False):
    test_one()

    p1_ = c.get_patron(p1['id'])
    assert (p1_is_correct(p1_))

    p3_ = c.get_patron(p3['id'])
    assert (p3_is_correct(p3_))

    # print_patron_info(c.get_patron(p1['id']))
    # print_patron_info(c.get_patron(p2['id']))
    return True


def test_four(info=False):
    test_two()
    assert (c.get_patron(p2['id']) == 'information no available, patron does not exist.')
    p3_ = c.get_patron(p3['id'])
    assert (p3_is_correct(p3_))
    print(c.get_patron(p2['id']))
    return True
    # print_patron_info(c.get_patron(p3['id']))


def test_five(info=False):
    test_two()
    try:
        c.check_out_doc(p2['id'], 1, 'book')
        return False
    except:
        print('Error,patron is not a patron of the library')
        return True


def test_six(info=False):
    test_two()
    c.check_out_doc(p1['id'], 1)
    c.check_out_doc(p3['id'], 2)
    c.check_out_doc(p1['id'], 2)
    # print_patron_info(c.get_patron(p1['id']))
    # print_patron_info(c.get_patron(p3['id']))
    p1_ = c.get_patron(p1['id'])
    assert (p1_is_correct(p1_) and len(eval((p1_['current_docs']))) == 2)

    p3_ = c.get_patron(p3['id'])
    assert (p3_is_correct(p3_) and len(eval((p3_['current_docs']))) == 1)
    return True


def test_seven(info=False):
    test_one()
    c.check_out_doc(p1['id'], 1)
    c.check_out_doc(p1['id'], 2)
    c.check_out_doc(p1['id'], 3)
    c.check_out_doc(p2['id'], 1)
    c.check_out_doc(p2['id'], 2)
    c.check_out_doc(p2['id'], 2, 'media')
    p1_ = c.get_patron(p1['id'])
    assert (p1_is_correct(p1_) and len(eval((p1_['current_docs']))) == 3)
    p2_ = c.get_patron(p2['id'])
    # print(p2)
    assert (p2_is_correct(p2_) and len(eval((p2_['current_docs']))) == 3)
    # print_patron_info(c.get_patron(p1['id']))
    # print_patron_info(c.get_patron(p2['id']))
    return True


def test_eight(info=False):
    test_one()
    c.check_out_doc(p1['id'], 1, date_when_took=datetime(2018, 2, 9))
    c.check_out_doc(p1['id'], 2, date_when_took=datetime(2018, 2, 2))
    c.check_out_doc(p2['id'], 1, date_when_took=datetime(2018, 2, 5))
    c.check_out_doc(p2['id'], 1, type_bd='media', date_when_took=datetime(2018, 2, 17))
    r1 = check_overdue(c.get_patron(p1['id']))
    r2 = check_overdue(c.get_patron(p2['id']))
    assert (len(r1) == 1 and len(r2) == 2)
    # print(check_overdue(c.get_patron(p1['id'])))
    # print(check_overdue(c.get_patron(p2['id'])))
    return True

#some_mistakes in the test (1 vmesto 3)
def test_nine():
    test_one()
    assert (d.get_label('free_count', 'book', 1) == 3 and  d.get_label('free_count', 'book', 2) == 2
            and d.get_label('free_count', 'book', 3) == 1 and d.get_label('count', 'media', 1) == 1
            and d.get_label('count', 'media', 2) == 1 and d.get_label('name', 'patrons', p1['id']) != None
            and d.get_label('name', 'patrons', p3['id']) != None
             and d.get_label('name', 'patrons', p2['id']) != None
            )
    return True
def main():
    while 1:
        print('Enter the number of the test:')
        r = int(input())
        if r == 1:
            print(test_one())
        if r == 2:
            print(test_two())
        if r == 3:
            print(test_three())
        if r == 4:
            print(test_four())
        if r == 5:
            print(test_five())
        if r == 6:
            print(test_six())
        if r == 7:
            print(test_seven())
        if r == 8:
            print(test_eight())
        if (r==9):
            print(test_nine())

main()
