import tornado
import hashlib
from logging import info, warning

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
        if errormsg: warning( errormsg)
        self.render( 'login.html', next=next, errormsg=errormsg)

    def post( self):
        login = self.get_argument( 'login', None)
        password = self.get_argument( 'password', None)

        if not password or not login:
            warning('didnt fill required fields')
            return self.get( "please enter both a name and a password")

        userobj = self.application.M.auth.find_one( {'login':login.lower()})
        if not userobj: 
            warning('user doesnt exist')
            return self.get( "Invalid login or password!")

        if not hashlib.sha256( password).hexdigest() == userobj['password']:
            warning('bad password')
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


        else:
            info( 'User exists, redirect to login')
            self.redirect( '/login') #user already exists
           
 
    def mkuser(self, **kwarg):
        self.application.M.auth.insert( dict(**kwarg))
        info( 'User created')
        return self.redirect('/')


