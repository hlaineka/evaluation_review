import sqlite3
from os import path
import json
import re
from intra import IntraAPIClient

ic = IntraAPIClient()

class StudentDatabase:
	def init_database(self, database_name):
		self.database = sqlite3.connect(database_name)
		self.cursor = self.database.cursor()
		self.cursor.execute("CREATE TABLE student(id INTEGER, login TEXT, url TEXT)")
		self.save_students()
	
	def __init__(self):
		if not (path.exists('./student.db')):
			self.init_database('./student.db')
		else:
			self.database = sqlite3.connect(database_name)
			self.cursor = self.database.cursor()

	def get_database(self):
		return self.database

	def get_cursor(self):
		return self.cursor

	def get_students(self):
		rows = self.cursor.execute("SELECT id, login, url FROM student").fetchall()
		return (rows)

	def get_student(self, login):
		student = self.cursor.execute("SELECT id, login, url FROM student WHERE login = wvaara")

	def save_student(self, student):
		self.cursor.execute("INSERT INTO student VALUES (?, ?, ?)", (student['id'], student['login'], student['url']))
		return

	def save_students(self):
		pattern = re.compile('3b3')
		response_list = ic.pages("campus/13/users")
		for i in response_list:
			print(i)
			for w in i:
				print(w)
				print(w['login'])
				try:
					if (pattern.search(w['login'])):
						continue
					else:
						self.save_student(w)
				except TypeError:
					break

	def testprint(self):
		logins = self.cursor.execute("SELECT login FROM student")
		for i in logins:
			print(i)

	
