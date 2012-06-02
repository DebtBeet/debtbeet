import tornado
import hashlib
from logging import info

class AuthHandler( tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("deadbeetuser")

    @property
    def user(self): return self.get_current_user()


class Logout( AuthHandler):
    def get(self):
        self.clear_cookie("deadbeetuser")
        self.redirect("/")

class Login( AuthHandler):
    def get( self, errormsg=None):
        next = self.get_argument("next", None)
        self.render( 'login.html', next=next, errormsg=errormsg)

    def post( self):
        login = self.get_argument( 'login', None)
        password = self.get_argument( 'password', None)

        if not password or not login:
            return self.get( "please enter both a name and a password")

        userobj = M[db].users.find_one( {'user':login.lower()})
        if not userobj: return self.get( "Invalid login or password!")

        if not sha512( password).hexdigest() == userobj['passhash']:
            return self.get( "Invalid login or password!" )

        self.set_secure_cookie("deadbeetuser", login)

        nexturl = self.get_argument('next', None)
        self.redirect( nexturl or '/')

class Signup( AuthHandler):
    def get( self, errormsg=None):
        self.render('signup.html', errormsg=errormsg)

    def post(self):

        login = self.get_argument('login')
        password = self.get_argument('password')
        password = hashlib.sha256(password).hexdigest() 
        phone = self.get_argument('phone')
        email = self.get_argument('email')

        #validation?!  hahaha, nope

        user = self.application.M.auth.find_one( {'login':login})
        if not user:
            return self.mkuser( login=login,password=password,phone=phone,email=email)

        #check password
        if user['password'] != password: return self.get( errormsg='Wrong Password')

        else:
            nxt = self.get_argument('next', '/')
            self.redirect( nxt)
            
    def mkuser(self, **kwarg):
        self.application.M.auth.insert( dict(**kwarg))





