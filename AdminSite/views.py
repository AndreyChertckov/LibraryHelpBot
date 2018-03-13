from flask import Blueprint,render_template,request

class Views:
    
    def __init__(self, app):
        self.blueprint = Blueprint('views',__name__)
        self.init_handlers()
        self.app = app
        self.app.register_blueprint(self.blueprint)

    def init_handlers(self):
        self.blueprint.add_url_rule('/','index',self.index)
        self.blueprint.add_url_rule('/signin','signin',self.signin_get,methods=['GET'])
        self.blueprint.add_url_rule('/signup','signup',self.signup_get,methods=['GET'])

    def index(self):
        session_ok = 'session_id' in request.cookies 
        return render_template('index.html',session_ok=session_ok)

    def signin_get(self):
        return render_template('signin.html')
    
    def signup_get(self):
        return render_template('signup.html')