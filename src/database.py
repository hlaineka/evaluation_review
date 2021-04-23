import sqlite3
from os import path
import json
import re
from intra import IntraAPIClient

ic = IntraAPIClient()

class StudentDatabase:	
	def __init__(self):
		if not (path.exists('./student.db')):
			self.database = sqlite3.connect('./student.db')
			cursor = self.database.cursor()
			self.database.execute("CREATE TABLE student(id INTEGER, login TEXT, url TEXT)")
			self.save_students()
			self.database.execute("CREATE TABLE scales(corrector TEXT, id INT, scale_id INT, comment TEXT, final_mark INT, begin_at DATETIME, corrected1 INT, corrected2 INT, corrected3 INT, corrected4 INT, filled_at DATETIME, duration INT, true_flags INT, feedback_comment TEXT, feedback_rating INT, feedback_id INT)")
			self.save_scale_teams()
			self.database.commit()

		else:
			self.database = sqlite3.connect('./student.db')
			self.database.commit()

	def get_database(self):
		return self.database

	def get_students(self):
		cursor = self.database.cursor()
		rows = cursor.execute("SELECT id, login, url FROM student")
		return (rows)

	def get_student(self, login):
		cursor = self.database.cursor()
		student = cursor.execute("SELECT id, login, url FROM student WHERE login = ?", (login, )).fetchone()
		return (student)

	def save_student(self, student):
		cursor = self.database.cursor()
		cursor.execute("INSERT INTO student (id, login, url) VALUES (?, ?, ?)", (student['id'], student['login'], student['url']))
		self.database.commit()
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
		return

	def	save_scale_team(self, team):
		cursor = self.database.cursor()
		cursor.execute("INSERT INTO scales (corrector, id, scale_id, comment, final_mark, begin_at, filled_at) VALUES (?, ?, ?, ?, ?, ?, ?)", ('hlaineka', team['id'], team['scale_id'], team['comment'], team['final_mark'], team['begin_at'], team['filled_at'], ))
		self.database.commit()
		return
	
	def save_student_teams(self):
		file = open('data.json')
		json_dump = file.read()
		data = json.loads(json_dump)
		for i in data:
			for w in i:
				self.save_scale_team(w)

	def	save_scale_teams(self):
		self.save_student_teams()


	
