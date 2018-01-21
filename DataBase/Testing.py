from UsersAndDocumentObjects.IBookingSystem import IBookingSystem
from UsersAndDocumentObjects.Document import  Document
from UsersAndDocumentObjects.Librarian import Librarian
from UsersAndDocumentObjects.Patron import Patron
from UsersAndDocumentObjects.Patron import PatronType
def main():
    p1=Patron("Vasya","UKRAIN","student",1,8999,[],[],2)
    p1.get_info()
main()