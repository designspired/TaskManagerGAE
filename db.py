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
			self.db = MySQLdb.connect(unix_socket=cloudsql_unix_socket, db=self.cloudsql_db, user=self.cloudsql_user, passwd=self.cloudsql_password)
		else:
			self.db = MySQLdb.connect(host='127.0.0.1', db=self.cloudsql_db, user=self.cloudsql_user, password=self.cloudsql_password)

	def registerNewUser(self, query):
		cursor = self.db.cursor()
		db = self.db
		try:
			cursor.execute(query)
			db.commit()
		except:
			db.rollback()
		
		row = cursor.fetchall()
		return row

	def __del__(self):
		self.connection.close()
