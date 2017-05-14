import os
import json
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
			return 'user already exists'

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

	def loginUser(self, email, password):
		query = """SELECT * FROM users WHERE email IN (%s)"""
		self.cursor.execute(query, [email])
		result = self.cursor.fetchall()
		for row in result:
			storedPassword = row['password']

		if password == storedPassword:
			uniqueId = row['unique_id']
			name = row['name']

			loginResult = {
				'uid': uniqueId,
				'name': name,
				'email': email,
				'password': password
			}

		else:
			loginResult = 'Wrong password.'

		return loginResult

	def changePassword(self, email, newPassword):
		query = """UPDATE users SET password=%s WHERE email=%s"""
		self.cursor.execute(query, [newPassword, email])

	def changeUsername(self, email, newName):
		query = """UPDATE users SET name=%s WHERE email=%s"""
		self.cursor.execute(query, [newName, email])

	def userAlreadyExists(self, email):
		query = """SELECT * FROM users WHERE email IN (%s)"""
		self.cursor.execute(query, [email])

		if self.cursor.rowcount >= 1:
			return True
		else:
			return False

	def __del__(self):
		self.connection.close()
