import datetime
import webapp2

from db import Database

db = Database()

class Register(webapp2.RequestHandler):
	def post(self):
		global db

		firebase_token = self.request.POST.get("firebase_token")
		name = self.request.POST.get("name")
		email = self.request.POST.get("email")	
		password = self.request.POST.get("password")
		uid = self.request.POST.get("uid")

		result = db.registerNewUser(uid, firebase_token, name, email, password)
		self.response.out.write(result)

class Login(webapp2.RequestHandler):
	def post(self):
		message = 'Hello'
		self.response.out.write(message)

class UploadImage(webapp2.RequestHandler):
	def post(self):
		pass

class FriendRequest(webapp2.RequestHandler):
	def post(self):
		pass

class Message(webapp2.RequestHandler):
	def post(self):
		pass

class LoadFriendsList(webapp2.RequestHandler):
	def post(self):
        global db
		uid = self.request.POST.get("uid")
        
		result = db.loadFriendsList(uid)
		self.response.out.write(result)


class SearchFriends(webapp2.RequestHandler):
	def post(self):
		pass

class UpdateUserInfo(webapp2.RequestHandler):
	def post(self):
		pass

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
