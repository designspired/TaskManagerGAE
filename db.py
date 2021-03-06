import os
import json
import MySQLdb
from friendstatus import FriendStatus

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

	def registerNewUser(self, uid, firebase_token, name, email, password):
		if Database.userAlreadyExists(self, email) == True:
			return 'user already exists'

		else:
			try:
				query = """INSERT INTO users (unique_id, firebase_token, name, email, password) VALUES (%s, %s, %s, %s, %s)"""
				self.cursor.execute(query, (uid, firebase_token, name, email, password))
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

	def userAlreadyExists(self, email):
		query = """SELECT * FROM users WHERE email IN (%s)"""
		self.cursor.execute(query, [email])

		if self.cursor.rowcount >= 1:
			return True
		else:
			return False

	def loadFriendsList(self, uid):
		query = """SELECT * FROM friends where sender_uid=%s OR receiver_uid=%s AND status=%s"""
        
		friendslist = list()
		status = FriendStatus()
		self.cursor.execute(query, [uid, uid, status.friend])

		friendsrow = self.cursor.fetchone()
		while friendsrow is not None:
			if uid == friendsrow['sender_uid']:
				friendUid = friendsrow['receiver_uid']
			elif uid == friendsrow['receiver_uid']:
				friendUid = friendsrow['sender_uid']
    
			fetch = """SELECT * FROM users WHERE unique_id IN (%s)"""
			self.cursor.execute(fetch, [friendUid])

			inforow = self.cursor.fetchone()
			while inforow is not None:
				row_array['uid'] = inforow['unique_id']
				row_array['name'] = inforow['name']
				row_array['email'] = inforow['email']
				friendslist.append(row_array)

		jsonlist = json.dumps(friendslist)
		return jsonlist

	def searchFriends(self, name):
		query = """SELECT unique_id, name, email FROM users WHERE name LIKE (%s)"""
		self.cursor.execute(query, [name])

		resultlist = list()
		resultrow = self.cursor.fetchone()
		while resultrow is not None:
			row_array['uid'] = resultrow['unique_id']
			row_array['name'] = resultrow['name']
			row_array['email'] = resultrow['email']
			resultlist.append(row_array)

		jsonlist = json.dumps(resultlist)
		return jsonlist

	def __del__(self):
		self.connection.close()
