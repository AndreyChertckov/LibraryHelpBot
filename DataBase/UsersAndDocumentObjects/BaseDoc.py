class BaseDoc:

    def __init__(self,id,authors,title,count,free_count,price,type):
        self.id=id;
        self.authors=authors
        self.name=title
        self.count=count
        self.free_count=free_count
        self.price=price
        self.type=type


    def get_id(self):
        return self.id

