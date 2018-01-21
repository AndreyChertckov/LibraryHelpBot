from UsersAndDocumentObjects.IBookingSystem import IBookingSystem
from UsersAndDocumentObjects.Document import  Document
from UsersAndDocumentObjects.Librarian import Librarian
from UsersAndDocumentObjects.Patron import Patron
from UsersAndDocumentObjects.Patron import PatronType
from BDmanagement import BDManagement
def main():
    #print all information in DataBase.db
    print("Data-base:")
    a=BDManagement()
    a.select_all()
main()