import sqlite3
from os import path
import json
import re
from intra import IntraAPIClient
from datetime import datetime

ic = IntraAPIClient()
timeformat = '%Y-%m-%dT%H:%M:%S.%fZ'

class StudentDatabase:
	#Function used to initialize the database. The creation takes time!
	def init_database(self):
		if not (path.exists('./student.db')):
			self.database = sqlite3.connect('./student.db')
			self.database.execute("CREATE TABLE tables (name TEXT, status INT, created DATETIME, updated DATETIME)")
			self.database.execute("INSERT INTO tables (name, status) VALUES (\"students\", 0), (\"scales\", 0), (\"projects\", 0), (\"student_points\", 0), (\"eval_points\", 0)")
			self.database.commit()
		else:
			self.database = sqlite3.connect('./student.db')
			self.database.commit()
		cursor = self.database.cursor()
		student_ready = cursor.execute("SELECT status FROM tables WHERE name = \"students\"").fetchone()
		if not (student_ready[0]):
			self.database.execute("drop table if exists students")
			self.database.execute("CREATE TABLE students(id INTEGER, login TEXT, url TEXT, total_points INT, evals INT, avarage_points INT)")
			self.save_students()
		projects_ready = cursor.execute("SELECT status FROM tables WHERE name = \"projects\"").fetchone()
		if not (projects_ready[0]):
			self.database.execute("drop table if exists projects")
			self.database.execute("CREATE TABLE projects (project_id INT, name TEXT, slug TEXT)")
			self.save_projects()
		scales_ready = cursor.execute("SELECT status FROM tables WHERE name = \"scales\"").fetchone()
		if not (scales_ready[0]):
			self.database.execute("drop table if exists scales")
			self.database.execute("CREATE TABLE scales(corrector TEXT, total_points INT DEFAULT 0, id INT, scale_id INT, project_id INT, comment TEXT, comment_points INT DEFAULT 0, final_mark INT, final_mark_points INT DEFAULT 0, begin_at DATETIME, corrected1 INT, corrected2 INT, corrected3 INT, corrected4 INT, too_friendly_points INT DEFAULT 0, filled_at DATETIME, duration INT, duration_points INT DEFAULT 0, true_flags INT, flags_points INT DEFAULT 0, feedback_comment TEXT, feedback_rating INT, feedback_id INT, feedback_points INT, feedback_total_points INT DEFAULT 0)")
			self.save_scale_teams()
		self.database.commit()

	def __init__(self):
		pass

	def get_database(self):
		return self.database

	def get_students(self):
		cursor = self.database.cursor()
		rows = cursor.execute("SELECT id, login, url FROM student")
		return (rows)

	def get_student(self, login):
		cursor = self.database.cursor()
		student = cursor.execute("SELECT id, login, url FROM students WHERE login = ?", (login, )).fetchone()
		return (student)

	def save_student(self, student):
		cursor = self.database.cursor()
		cursor.execute("INSERT INTO students (id, login, url) VALUES (?, ?, ?)", (student['id'], student['login'], student['url']))
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
		time = datetime.now().strftime("%B %d, %Y %I:%M%p")
		cursor.execute("UPDATE tables SET status = 1, created = (?) WHERE name = \"students\"", (time, ))
		self.database.commit()
		return

	def	get_comment_points(self, team):
		comment_len = len(team['comment'])
		comment_points = 0
		if (comment_len > 180):
			comment_points = 1
		return comment_points

	def	get_final_mark_points(self):
		return 0

	def get_too_friendly_points(self):
		return 0

	def get_duration_points(self, team, final_mark_points):
		start_time = datetime.strptime(team['begin_at'], timeformat)
		end_time = datetime.strptime(team['filled_at'], timeformat)
		target_time = team['scale']['duration']
		minimum_time = target_time * 0.66
		duration = (end_time - start_time).total_seconds()
		duration_points = 0
		if (duration < minimum_time and final_mark_points > 0):
			duration_points = -42
		elif duration < target_time:
			duration_points = -10
		elif duration > target_time * 1.5:
			duration_points = 20
		else:
			duration_points = 10
		return duration_points

	def calculate_eval_points(self, scale_id, team):
		final_mark_points = self.get_final_mark_points()
		self.database.execute("UPDATE scales SET final_mark_points ="+str(final_mark_points)+" WHERE scale_id = (?)", (scale_id, ))
		comment_points = self.get_comment_points(team)
		self.database.execute("UPDATE scales SET comment_points = 1 WHERE scale_id = (?)", (scale_id, ))
		too_friendly_points = self.get_too_friendly_points()
		self.database.execute("UPDATE scales SET too_friendly_points ="+str(too_friendly_points)+" WHERE scale_id = (?)", (scale_id, ))
		duration_points = self.get_duration_points(team, final_mark_points)
		self.database.execute("UPDATE scales SET too_friendly_points ="+str(too_friendly_points)+" WHERE scale_id = (?)", (scale_id, ))
		flags_points = 0
		feedback_total_points = 0
		total_points = comment_points + final_mark_points + too_friendly_points + duration_points + flags_points + feedback_total_points
		self.database.execute("UPDATE scales SET too_friendly_points ="+str(total_points)+" WHERE scale_id = (?)", (scale_id, ))
		self.database.commit()

	def	save_scale_team(self, team):
		# checking that the evaluation did actually happen
		if not team['filled_at']:
			return
		scale_id = team['id']
		feedback_id = team['feedbacks'][0]['id']
		cursor = self.database.cursor()
		cursor.execute("INSERT INTO scales (corrector, id, scale_id, project_id, comment, final_mark, begin_at, filled_at, duration, feedback_comment, feedback_rating, feedback_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ('hlaineka', team['id'], team['scale_id'], team['team']['project_id'], team['comment'], team['final_mark'], team['begin_at'], team['filled_at'], team['scale']['duration'], team['feedbacks'][0]['comment'], team['feedbacks'][0]['rating'], team['feedbacks'][0]['id'] ))
		# detailed info on the feedback rating points
		url = "feedbacks/"+str(feedback_id)
		response = ic.get(url)
		data = response.json()
		feedback_points = 0
		for i in (data['feedback_details']):
			feedback_points += i['rate']
		executable = "UPDATE scales SET feedback_points = "+str(feedback_points)+" WHERE id = "+str(scale_id)
		cursor.execute(executable)
		i = 0
		# adding the correcteds
		for person in team['correcteds']:
			if (i < 3):
				executable = "UPDATE scales SET corrected"+str(i+1)+" = \""+person['login']+"\" WHERE id = "+str(scale_id)
				cursor.execute(executable)
			i += 1
		self.calculate_eval_points(scale_id, team)
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
		time = datetime.now().strftime("%B %d, %Y %I:%M%p")
		self.database.execute("UPDATE tables SET status = 1, created = (?) WHERE name = \"scales\"", (time, ))
		self.database.commit()

	def	save_project(self, project):
		for i in project:
			for w in (i['campus']):
				if (w['id'] == 13):
					self.database.execute("INSERT INTO projects (project_id, name, slug) VALUES (?, ?, ?)", (i['id'], i['name'], i['slug']))
		self.database.commit()
	
	def save_projects(self):
		response_list = ic.pages("cursus/1/projects")
		for i in response_list:
			self.save_project(i)
		time = datetime.now().strftime("%B %d, %Y %I:%M%p")
		self.database.execute("UPDATE tables SET status = 1, created = (?) WHERE name = \"projects\"", (time, ))
		self.database.commit()


	
