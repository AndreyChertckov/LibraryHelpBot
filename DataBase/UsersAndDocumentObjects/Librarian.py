from UsersAndDocumentObjects.user import userBase
from BDTables import BDTables

class Librarian(userBase):
    __metaclass__ = type

    def __init__(self, name, address, id, phone):
        userBase.__init__(self,name,address,"librarian",id,phone)
        BDTables.bd.add_librarian(self)
        # additional information

    def edit_document(self, docId): pass

    def add_document(self, newdoc): pass

    def delete_document(self, docId): pass

    def get_info(self):

        return (int(self.get_id()),self.get_name(),self.get_phone(),self.get_address(),self.get_type())