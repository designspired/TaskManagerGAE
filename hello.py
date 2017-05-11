import webapp2

class Hello(webapp2.RequestHandler):
	def post(self):
		self.response.out.write('hello')

application = webapp2.WSGIApplication(['/hello', Hello], debug=True)
