import sys; sys.path.append('lib/')

import os
join = os.path.join
exists = os.path.exists

from logging import info
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import HTTPError
from markdown import markdown

import pymongo
import stripe
db = 'debtbeet'

from auth import AuthHandler

class App( tornado.web.Application):
    def __init__(self):
        """
        Settings for our application
        """
        settings = dict(
            cookie_secret="changemeplz",
            login_url="/login", 
            template_path= "templates",
            static_path= "static",
            xsrf_cookies= False,
            debug = True, #autoreloads on changes, among other things
        )

        """
        map URLs to Handlers, with regex patterns
        """
   
        from auth import Signup, Login, Logout
 
        handlers = [
            (r"/", MainHandler),
            (r"/signup", Signup),
            (r"/login", Login),
            (r"/debt", DebtHandler),
            (r"/tour", TourHandler),
            (r"/about", AboutHandler),
            (r"/payment", PaymentHandler),
            (r"/dashboard", DashboardHandler),
            (r"/styletest", Test),
            (r"(?!\/static.*)(.*)/?", DocHandler),
            #(r"(.*)/?", DocHandler),
        ]

        self.M = pymongo.Connection()[db]

        tornado.web.Application.__init__(self, handlers, **settings)



class MainHandler( AuthHandler):
    def get(self):
        if self.user: info(self.user)
        self.render( 'index.html')


class AboutHandler( tornado.web.RequestHandler):
    def get(self):
        self.render( 'about.html')

class TourHandler( tornado.web.RequestHandler):
    def get(self):
        self.render( 'tour.html')


class PaymentHandler( tornado.web.RequestHandler):
    def get(self):
        self.render( 'payment.html')

    def post(self):
        # set your secret key: remember to change this to your live secret key in production
        # see your keys here https://manage.stripe.com/account
        stripe.api_key = "JRRtYhu65g1qmK6CnJSGnrGURYfgXktv"

        # get the credit card details submitted by the form
        token = self.get_argument('stripeToken')

        # Explode the price
        price = self.get_argument('amount')
        price = price.strip(',')
        float( price)
        if '.' in price:
            dollars, cents = price.split('.')
            dollars = int(dollars)*100
            dollars += int(cents)

            cents = dollars

        else:
            cents = int(price) *100




        # create the charge on Stripe's servers - this will charge the user's card
        charge = stripe.Charge.create(
            amount=cents, # amount in cents, again
            currency="usd",
            card=token,
            description="payinguser@example.com"
            )

        self.application.M.payments.insert( charge)

        self.redirect( '/payment')


class DashboardHandler( tornado.web.RequestHandler):
    def get(self):
        self.render( 'dashboard.html')

class Test( tornado.web.RequestHandler):
    def get(self):
        self.render( 'test.html')


class DocHandler( tornado.web.RequestHandler):
    def get(self, path):

        path = 'docs/' + path.replace('.', '').strip('/')
        if exists( path):
            #a folder
            lastname = os.path.split(path)[-1]
            txt = open( '%s/%s.txt'%( path, lastname)).read()

        elif exists( path+'.txt'):
            txt = open( path+'.txt').read()

        else:
            self.redirect('/')

        doc = markdown( txt)
        self.render( 'doc.html', doc=doc) 


class DebtHandler( AuthHandler):
    def get(self):
        #render a pie chart somehow
        self.render( 'pie.html')
        pass

    def post(self):
        """
        takes: totalamount, N users, N amounts
        """
        debtbeets = {}

        for i in range( int( self.get_argument('beetcounter'))+1  ):
            user = self.get_argument( 'debtbeet%d'%i)
            owes = float( self.get_argument( 'owes%d'%i))
            debtbeets[user] = owes

        self.get()




def main():
    from tornado.options import define, options
    define("port", default=8001, help="run on the given port", type=int)
    define("runtests", default=False, help="run tests", type=bool)

    tornado.options.parse_command_line()

    if options.runtests:
        #put tests in the tests folder
        import tests, unittest
        import sys
        sys.argv = ['dojoserv.py',] #unittest goes digging in argv
        unittest.main( 'tests')
        return

    http_server = tornado.httpserver.HTTPServer( App() )
    http_server.listen(options.port)
    info( 'Serving on port %d' % options.port )
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

