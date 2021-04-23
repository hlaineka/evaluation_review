import bottle
from bottle import route, run, template
from database import StudentDatabase

class WebInterface:
	def __init__ (self):
		self.student_database = StudentDatabase('students.db')

	# gets all the students at Hive Helsinki
	def get_index(self):
		data = self.student_database.get_students()
		if data:
			return template('index', students=data)
		else:
			return HTTPResponse(status=204)