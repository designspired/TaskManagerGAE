import datetime
import webapp2
import json
import MySQLdb

from hello2 import Hello

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
		
		self.response.out.write(jsondata)

class Login(webapp2.RequestHandler):
	def post(self):
		message = 'Hello'
		self.response.out.write(message)

application = webapp2.WSGIApplication([
	('/register', Register),
	('/login', Login)
	], debug=True)
