from UsersAndDocumentObjects.user import userBase


class Librarian(userBase):
    __metaclass__ = type

    def __init__(self, name, address, type, id, phone):
        userBase.__init__(name, address, type, id, phone)
        # additional information

    def edit_document(self, docId): pass

    def add_document(self, newdoc): pass

    def delete_document(self, docId): pass
