import datetime
import webapp2
import json
import MySQLdb
import pyfcm
import uuid

from hello2 import Hello
from db import Database

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

		uniqueId = str(uuid.uuid4())
		currentTime = datetime.datetime.now()

		db = Database()

		result = db.registerNewUser(uniqueId, name, email, password)

		jsondata = json.dumps(userdata) 
		
		self.response.out.write(result)

class Login(webapp2.RequestHandler):
	def post(self):
		message = 'Hello'
		self.response.out.write(message)

application = webapp2.WSGIApplication([
	('/register', Register),
	('/login', Login)
	], debug=True)
