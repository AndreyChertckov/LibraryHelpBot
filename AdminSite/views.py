from flask import Blueprint,render_template,request, redirect

from AdminSite.utils import check_session

class Views:
    
    def __init__(self, app, api, dbmanager):
        self.blueprint = Blueprint('views',__name__)
        self.init_handlers()
        self.app = app
        self.app.register_blueprint(self.blueprint)
        self.dbmanager = dbmanager

    def init_handlers(self):
        self.blueprint.add_url_rule('/','index',self.index)
        self.blueprint.add_url_rule('/signin','signin',self.signin_get,methods=['GET'])
        self.blueprint.add_url_rule('/signup','signup',self.signup_get,methods=['GET'])

    def index(self):
        session_ok = 'session_id' in request.cookies and check_session(request.cookies['session_id'],self.dbmanager)
        if not session_ok:
            return redirect('/signin')
        return render_template('index.html')

    def signin_get(self):
        error = True if ('error' in request.cookies) and (request.cookies['error'] == 'Login error') else False
        response = self.app.make_response(render_template('signin.html',error = error))
        if ('error' in request.cookies) and (request.cookies['error'] == 'Login error'): 
            response.delete_cookie('error')
        return response
    
    def signup_get(self):
        if 'verification_string' in request.args and self.dbmanager.if_verification_string_exist(request.args.get('verification_string'),1):
            return render_template('signup.html')
        else:
            return 'Please write to admin to get signup link.'