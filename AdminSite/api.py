from flask import Flask

class API:

    def __init__(self, controller):
        self.app = Flask(__name__)
        self.cntrl = controller
        self.app.add_url_rule('/','index',test)
    
    def run(self):
        self.app.run()

def test():
    return 'Hello world'