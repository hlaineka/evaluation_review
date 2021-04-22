import sqlite3
from os import path

class StudentDatabase:
	def __init__(self, database_name):
		if (path.exists(database_name)):
			#dbfile = open(database_name)
			self.database = sqlite3.connect(database_name)
			self.cursor = self.database.cursor()
		else:
			self.database = sqlite3.connect(database_name)
			self.cursor = self.database.cursor()
			self.cursor.execute("CREATE TABLE student(id INTEGER, login TEXT, url TEXT)")

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

	def students_added(self):
		rows = self.get_students()
		if not rows:
			return False
		return True
