import os
import MySQLdb

class Database:

	def __init__(self):
		self.cloudsql_connection_name = os.environ.get('CLOUDSQL_CONNECTION_NAME')
		self.cloudsql_user = os.environ.get('CLOUDSQL_USER')
		self.cloudsql_db = os.environ.get('CLOUDSQL_DB')
		self.cloudsql_password = os.environ.get('CLOUDSQL_PASSWORD')

		if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
			cloudsql_unix_socket = os.path.join('/cloudsql', self.cloudsql_connection_name)
			self.connection = MySQLdb.connect(unix_socket=cloudsql_unix_socket, db=self.cloudsql_db, user=self.cloudsql_user, passwd=self.cloudsql_password)
			self.cursor = self.connection.cursor()
		else:
			self.connection = MySQLdb.connect(host='127.0.0.1', db=self.cloudsql_db, user=self.cloudsql_user, password=self.cloudsql_password)
			self.cursor = self.connection.cursor()

	def registerNewUser(self, uniqueId, name, email, password):

		if Database.userAlreadyExists(self, email) == True:
			return 'user_already_exists'

		else:
			try:
				query = """INSERT INTO users (unique_id, name, email, password) VALUES (%s, %s, %s, %s)"""
				self.cursor.execute(query, (uniqueId, name, email, password))
				self.connection.commit()
				return 'success'

			except:
				self.connection.rollback()
				return 'failure'

			finally:
				self.cursor.close()

			self.connection.close()

	def userAlreadyExists(self, email):
		query = """SELECT * FROM users WHERE email IN (%s)"""
		self.cursor.execute(query, [email])

		if self.cursor.rowcount >= 1:
			return True
		else:
			return False

	def __del__(self):
		self.connection.close()
