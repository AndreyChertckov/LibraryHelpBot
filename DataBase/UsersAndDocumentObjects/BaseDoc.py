# Base class for all types of materials

class BaseDoc:
    # Initialization
    # Params:id (int) , authors , title, count, free_count(available count),price,type
    def __init__(self,id,authors, title, count, free_count, price, type,keywords):
        self.id=id
        self.authors = authors
        self.name = title
        self.count = count
        self.free_count = free_count
        self.price = price
        self.type = type
        self.keywords=keywords

