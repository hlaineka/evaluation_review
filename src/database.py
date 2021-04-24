import sqlite3
from os import path
import json
import re
from intra import IntraAPIClient

ic = IntraAPIClient()

class StudentDatabase:
	def init_database(self):
		cursor = self.database.cursor()
		student_ready = cursor.execute("SELECT status FROM tables WHERE name = \"student\"").fetchone()
		if not student_ready[0]:
			self.database.execute("CREATE TABLE student(id INTEGER, login TEXT, url TEXT)")
			self.save_students()
		scales_ready = cursor.execute("SELECT status FROM tables WHERE name = \"scales\"").fetchone()
		if not scales_ready[0]:
			self.database.execute("drop table if exists scales")
			self.database.execute("CREATE TABLE scales(corrector TEXT, id INT, scale_id INT, comment TEXT, final_mark INT, begin_at DATETIME, corrected1 INT, corrected2 INT, corrected3 INT, corrected4 INT, filled_at DATETIME, duration INT, true_flags INT, feedback_comment TEXT, feedback_rating INT, feedback_id INT)")
			self.save_scale_teams()
		self.database.commit()

	def __init__(self):
		if not (path.exists('./student.db')):
			self.database = sqlite3.connect('./student.db')
			self.database.execute("CREATE TABLE tables (name TEXT, status INT)")
			self.database.execute("INSERT INTO tables (name, status) VALUES (\"student\", 0), (\"scales\", 0)")
			self.database.commit()
		else:
			self.database = sqlite3.connect('./student.db')
			self.database.commit()
		self.init_database()

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
		cursor = self.database.cursor()
		cursor.execute("UPDATE tables SET status = 1 WHERE name = \"student\"")
		return

	def	save_scale_team(self, team):
		# checking that the evaluation did actually happen
		if not team['filled_at']:
			return
		scale_id = team['id']
		cursor = self.database.cursor()
		print(team['feedbacks'][0]['comment']) 
		print(team['feedbacks'][0]['rating'])
		print(team['feedbacks'][0]['id'])
		cursor.execute("INSERT INTO scales (corrector, id, scale_id, comment, final_mark, begin_at, filled_at, duration, feedback_comment, feedback_rating, feedback_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ('hlaineka', team['id'], team['scale_id'], team['comment'], team['final_mark'], team['begin_at'], team['filled_at'], team['scale']['duration'], team['feedbacks'][0]['comment'], team['feedbacks'][0]['rating'], team['feedbacks'][0]['id'] ))
		self.database.commit()
		i = 0
		for person in team['correcteds']:
			if (i < 3):
				executable = "UPDATE scales SET corrected"+str(i+1)+" = \""+person['login']+"\" WHERE id = "+str(scale_id)
				cursor.execute(executable)
			i += 1
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


	
