import MySQLdb

class Database:

	host = '/cloudsql/task-manager-marshall:taskmanagergae'
	db = 'taskmanager'
	user = 'root'
	passwd = 'SantaClaus1225^^'

	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.db, self.user, self.passwd)
		self.cursor = self.connection.cursor()

	def registerNewUser(self, query):
		try:
			self.cursor.execute(query)
			self.connection.commit()
		except:
			self.connection.rollback()

	def __del__(self):
		self.connection.close()
