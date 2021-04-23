import sqlite3
from os import path
import json
import re
from intra import IntraAPIClient

ic = IntraAPIClient()

class StudentDatabase:
	def __init__(self, database_name):
		if (path.exists(database_name)):
			self.database = sqlite3.connect(database_name)
			self.cursor = self.database.cursor()
		else:
			self.database = sqlite3.connect(database_name)
			self.cursor = self.database.cursor()
			self.init_database()

	def init_database(self):
		self.cursor.execute("CREATE TABLE student(id INTEGER, login TEXT, url TEXT)")
		self.save_students()

	def get_database(self):
		return self.database

	def get_cursor(self):
		return self.cursor

	def get_students(self):
		rows = self.cursor.execute("SELECT id, login, url FROM student").fetchall()
		return (rows)

	def save_student(self, student):
		self.cursor.execute("INSERT INTO student VALUES (?, ?, ?)", (student['id'], student['login'], student['url']))
		return

	def save_students(self):
		pattern = re.compile('3b3')
		response_list = ic.pages("campus/13/users")
		for i in response_list:
			for w in i:
				try:
					if (pattern.search(w['login'])):
						continue
					else:
						self.save_student(w)
				except TypeError:
					break

	def students_added(self):
		rows = self.get_students()
		if not rows:
			return False
		return True
