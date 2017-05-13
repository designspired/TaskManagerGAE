import datetime
import webapp2

class Register(webapp2.RequestHandler):
	def post(self):
		name = self.request.POST.get("name")
		self.response.out.write(name)

class Login(webapp2.RequestHandler):
	def post(self):
		message = 'Hello'
		self.response.out.write(message)

application = webapp2.WSGIApplication([
	('/register', Register),
	('/login', Login)
	], debug=True)
