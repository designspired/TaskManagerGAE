import os
import datetime
import webapp2
import json
import MySQLdb
import pyfcm
import uuid

from hello2 import Hello

# Cloud SQL Instance
_instance = 'task-manager-marshall:asia-east1:taskmanagergae'

db = MySQLdb.connect(unix_socket='/cloudsql/' + _instance, db='taskmanager', user='root', password='SantaClaus1225^^', charset='utf-8')

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
		
		uniqueId = uuid.uuid4()
		self.response.out.write(uniqueId)

class Login(webapp2.RequestHandler):
	def post(self):
		message = 'Hello'
		self.response.out.write(message)

application = webapp2.WSGIApplication([
	('/register', Register),
	('/login', Login)
	], debug=True)
