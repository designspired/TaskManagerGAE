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

		uniqueId = uuid.uuid4()
		currentTime = datetime.datetime.now()

		db = Database()

		i = db.registerNewUser(uuid, name, email, password, currentTime)

		jsondata = json.dumps(userdata) 
		
		self.response.out.write(uniqueId)

class Login(webapp2.RequestHandler):
	def post(self):
		message = 'Hello'
		self.response.out.write(message)

application = webapp2.WSGIApplication([
	('/register', Register),
	('/login', Login)
	], debug=True)
