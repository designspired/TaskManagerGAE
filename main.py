import datetime
import webapp2
import json
import MySQLdb
import hello2

class Register(webapp2.RequestHandler):
	def post(self):
		name = self.request.POST.get("name")
		email = self.request.POST.get("email")		
		
		password = self.request.POST.get("password")

		userdata = {
			'name': name,
			'email': email,
			'password': password
		}

		jsondata = json.dumps(userdata)

		i = Hello()
		j = i.call() 
		
		self.response.out.write(j)

class Login(webapp2.RequestHandler):
	def post(self):
		message = 'Hello'
		self.response.out.write(message)

application = webapp2.WSGIApplication([
	('/register', Register),
	('/login', Login)
	], debug=True)
