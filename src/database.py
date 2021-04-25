import sqlite3
from os import path
import json
import re
from intra import IntraAPIClient
from datetime import datetime

ic = IntraAPIClient()
timeformat = '%Y-%m-%dT%H:%M:%S.%fZ'
timeformat_sql = '%Y-%m-%d %H:%M:%S'

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
			self.database.execute("CREATE TABLE scales(corrector TEXT, total_points INT DEFAULT 0, id INT, scale_id INT, project_id INT, comment TEXT, comment_points INT DEFAULT 0, final_mark INT, final_mark_points INT DEFAULT 0, begin_at DATETIME, corrected1 TEXT, corrected2 TEXT, corrected3 TEXT, corrected4 INT, too_friendly_points INT DEFAULT 0, filled_at DATETIME, duration INT, duration_points INT DEFAULT 0, true_flags INT, flags_points INT DEFAULT 0, feedback_comment TEXT, feedback_rating INT, feedback_id INT, feedback_points INT, feedback_interested INT, feedback_nice INT, feedback_punctuality INT, feedback_rigorous INT, feedback_total_points INT DEFAULT 0)")
			self.save_scale_teams()
		self.database.commit()

	def __init__(self):
		self.database = None

	#getter for others to use
	def get_database(self):
		return self.database

	def get_students(self):
		cursor = self.database.cursor()
		rows = cursor.execute("SELECT id, login, url FROM students")
		return (rows)

	def get_student(self, login):
		cursor = self.database.cursor()
		student = cursor.execute("SELECT id, login, url FROM students WHERE login = ?", (login, )).fetchone()
		return (student)

	def get_eval(self, id):
		cursor = self.database.cursor()
		one_eval = cursor.execute("SELECT corrector, total_points, id, project_id, comment, comment_points, final_mark, final_mark_points, begin_at, corrected1, corrected2, corrected3, corrected4, too_friendly_points, duration, duration_points, flags_points, feedback_comment, feedback_points, feedback_total_points FROM scales WHERE id ="+str(id)).fetchone()
		return one_eval

	def get_evals(self, start = 0, amount = 20, order = 'total_points', start_date = None, end_date = None):
		cursor = self.database.cursor()
		if (end_date is None and start_date is None):
			evals = cursor.execute("SELECT total_points, id, project_id, begin_at, corrector, corrected1, corrected2, corrected3, corrected4 FROM scales ORDER BY "+order+" LIMIT "+str(amount)+" OFFSET "+str(start))
		else:
			evals = cursor.execute("SELECT total_points, id, project_id, begin_at, corrector, corrected1, corrected2, corrected3, corrected4 FROM scales WHERE begin_at BETWEEN "+start_date+" AND "+end_date+" ORDER BY "+order+" OFFSET "+str(start)+" ROWS FETCH NEXT "+str(amount)+"ROWS ONLY")
		return evals

	def get_project_name(self, id):
		project = self.database.execute("SELECT slug FROM projects WHERE project_id = "+str(id)).fetchone()
		project_name = project[0]
		return (project_name)


	#student database creation
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
		time = datetime.now().strftime(timeformat_sql)
		cursor.execute("UPDATE tables SET status = 1, created = (?) WHERE name = \"students\"", (time, ))
		self.database.commit()
		return

	#point calculation for evals
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

	def get_feedback_total_points(self, feedback_points):
		return (feedback_points * 2)

	def calculate_eval_points(self, scale_id, team, feedback_points):
		cursor = self.database.cursor()
		final_mark_points = self.get_final_mark_points()
		cursor.execute("UPDATE scales SET final_mark_points ="+str(final_mark_points)+" WHERE id = (?)", (scale_id, ))
		comment_points = self.get_comment_points(team)
		cursor.execute("UPDATE scales SET comment_points = 1 WHERE id = (?)", (scale_id, ))
		too_friendly_points = self.get_too_friendly_points()
		cursor.execute("UPDATE scales SET too_friendly_points ="+str(too_friendly_points)+" WHERE id = (?)", (scale_id, ))
		duration_points = self.get_duration_points(team, final_mark_points)
		cursor.execute("UPDATE scales SET duration_points ="+str(duration_points)+" WHERE id = (?)", (scale_id, ))
		flags_points = 0
		feedback_total_points = self.get_feedback_total_points(feedback_points)
		cursor.execute("UPDATE scales SET feedback_total_points ="+str(feedback_total_points)+" WHERE id = (?)", (scale_id, ))
		total_points = comment_points + final_mark_points + too_friendly_points + duration_points + flags_points + feedback_total_points
		cursor.execute("UPDATE scales SET total_points ="+str(total_points)+" WHERE id = (?)", (scale_id, ))
		self.database.commit()

	#scale teams database creations
	def	save_scale_team(self, team):
		# checking that the evaluation did actually happen
		if not team['filled_at']:
			return
		#adding only evaluations that happened after c-piscine for the test version, well this does now work :D
		project = self.database.execute("SELECT name FROM projects WHERE project_id = "+str(team['team']['project_id'])).fetchone()
		if not project:
			return
		scale_id = team['id']
		feedback_id = team['feedbacks'][0]['id']
		start_time = datetime.strptime(team['begin_at'], timeformat)
		end_time = datetime.strptime(team['filled_at'], timeformat)
		begin_str = start_time.strftime(timeformat_sql)
		filled_str = end_time.strftime(timeformat_sql)
		cursor = self.database.cursor()
		cursor.execute("INSERT INTO scales (corrector, id, scale_id, project_id, comment, final_mark, begin_at, filled_at, duration, feedback_comment, feedback_rating, feedback_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ('hlaineka', team['id'], team['scale_id'], team['team']['project_id'], team['comment'], team['final_mark'], begin_str, filled_str, team['scale']['duration'], team['feedbacks'][0]['comment'], team['feedbacks'][0]['rating'], team['feedbacks'][0]['id'] ))
		# detailed info on the feedback rating points
		url = "feedbacks/"+str(feedback_id)
		response = ic.get(url)
		data = response.json()
		feedback_points = 0
		for i in (data['feedback_details']):
			cursor.execute("UPDATE scales SET feedback_"+i['kind']+" = "+str(i['rate'])+" WHERE id = "+str(scale_id))
			feedback_points += i['rate']
		executable = "UPDATE scales SET feedback_points = "+str(feedback_points)+" WHERE id = "+str(scale_id)
		cursor.execute(executable)
		cursor.execute('UPDATE scales SET feedback_comment = (?) WHERE id = '+str(scale_id), (data['comment'], ))
		i = 0
		# adding the correcteds
		for person in team['correcteds']:
			if (i < 4):
				executable = "UPDATE scales SET corrected"+str(i+1)+" = \""+person['login']+"\" WHERE id = "+str(scale_id)
				cursor.execute(executable)
			i += 1
		self.calculate_eval_points(scale_id, team, feedback_points)
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
		time = datetime.now().strftime(timeformat_sql)
		self.database.execute("UPDATE tables SET status = 1, created = (?) WHERE name = \"scales\"", (time, ))
		self.database.commit()

	#project database creation
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
		time = datetime.now().strftime(timeformat_sql)
		self.database.execute("UPDATE tables SET status = 1, created = (?) WHERE name = \"projects\"", (time, ))
		self.database.commit()


	
