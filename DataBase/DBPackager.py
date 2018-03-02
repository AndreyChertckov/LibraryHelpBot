class Packager:

    def __init__(self, parametrs):
        self.attrs = parametrs.keys()
        for i in parametrs.items():
            setattr(self, *i)

    def get_info(self):
        return [getattr(self, i) for i in self.attrs]

