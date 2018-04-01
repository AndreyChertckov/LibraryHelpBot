from DataBase.DBmanager import Manager
from DataBase.DBPackager import Packager
from Controller.controller import Controller
m=Manager()
c=Controller()

b2 = {'title': 'Design Patterns: Elements of Reusable Object-Oriented Software',
      'authors': ': Erich Gamma, Ralph Johnson, John Vlissides, Richard Helm',
      'description': 'OOP as design-pattern. Addison-Wesley Professional 2003.First edition', 'count': 3,
      'free_count': 3, 'price': 1000,
      'best_seller': 1,
      'keywords': 'OOP,programming'}
p1 = {'id': 1, 'name': 'Sergey Afonso', 'address': 'Via Margutta, 3',
      'status': 'Student', 'phone': '30001', 'history': [], 'current_docs': []}

j1 = {'title': 'Journal_Ref1', 'authors': 'Ya,On,Ona', 'keywords': 'journals',
      'issue': 1999, 'editors': 'MIT science', 'date': '02.12.33', 'journal': 'MGU'}

ref_book_1={'title': 'Design Patterns: Elements of Reusable Object-Oriented Software',
      'authors': ': Erich Gamma, Ralph Johnson, John Vlissides, Richard Helm',
      'description': 'OOP as design-pattern. Addison-Wesley Professional 2003.First edition',
      'keywords': 'OOP,programming'}

def test_bd_add_ref_article():
      #(title,authors,journal,keywords,issue,editors,date)
      m.clear_table('reference_article')
      m.add_reference_article(Packager(j1))
      assert(m.get_count('reference_article')==1)

def test_bd_add_ref_book():
      m.clear_table('reference_book')
      m.add_reference_book(Packager(ref_book_1))
      assert (m.get_count('reference_book')==1)

def test_controller_add_ref_book():
      m.clear_table('reference_book')
      c.add_document(ref_book_1,'reference_book')
      assert (len(c.get_all_reference_book())==1)

def test_controller_add_ref_article():
      m.clear_table('reference_article')
      c.add_document(j1,'reference_article')
      assert (len(c.get_all_reference_articles()) == 1)

def test_add_queue_order():
      #m.clear_table('patrons')
     # m.clear_table('book')
      try:
            m.add_patron(Packager(p1))
      except:
            print('Warning!Patron already added')

      c.add_document(b2,'book')
      book_id=m.get_max_id('book')
      c.add_queue_order(1,'book', book_id)

      assert(len(c.get_user_queue(1))>1)
      assert(len(eval(m.get_label('queue','book', book_id))[0])==1)

def test_renew_item():
      c.add_document(b2,'book')
      book_id = m.get_max_id('book')
      c.check_out_doc(1,book_id,'book')
      c.renew_item(1,'book',book_id)
      c.renew_item(1, 'book', book_id)
      assert (m.get_label('renewed','orders',m.get_max_id('orders'))==1)

def test_delete_user_queue():
      c.delete_user_queue(1,'book',2)
#test_bd_add_ref_article()
#test_bd_add_ref_book()
#test_controller_add_ref_article()
#test_controller_add_ref_book()
#test_add_queue_order()
test_renew_item()
#test_delete_user_queue()