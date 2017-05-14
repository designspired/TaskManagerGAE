import datetime
import webapp2
import json
import MySQLdb
import pyfcm

from hello2 import Hello
from db import Database

class Register(webapp2.RequestHandler):
	def post(self):
		name = self.request.POST.get("name")
		email = self.request.POST.get("email")				
		password = self.request.POST.get("password")
		uid = self.request.POST.get("uid")

		db = Database()

		result = db.registerNewUser(uid, name, email, password)

		self.response.out.write('bye')

class Login(webapp2.RequestHandler):
	def post(self):
		message = 'Hello'
		self.response.out.write(message)

class UploadImage(webapp2.RequestHandler):
	def post(self):


class FriendRequest(webapp2.RequestHandler):
	def post(self):

class Message(webapp2.RequestHandler):
	def post(self):

class LoadFriendsList(webapp2.RequestHandler):
	def post(self):

class SearchFriends(webapp2.RequestHandler):
	def post(self):

class UpdateUserInfo(webapp2.RequestHandler):
	def post(self):

application = webapp2.WSGIApplication([
	('/register', Register),
	('/login', Login),
	('/uploadimage', UploadImage),
	('/friendrequest', FriendRequest),
	('/message', Message),
	('/loadfriendslist', LoadFriendsList),
	('/searchfriends', SearchFriends),
	('/updateuserinfo', UpdateUserInfo)
	], debug=True)
