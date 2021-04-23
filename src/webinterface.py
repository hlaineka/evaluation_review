import bottle
from bottle import route, run, template
from database import StudentDatabase

class WebInterface:
	def __init__ (self, studentdb):
		self.student_database = studentdb

	# gets all the students at Hive Helsinki
	def get_index(self):
		data = self.student_database.get_students()
		if data:
			return template('index', students=data)
		else:
			return HTTPResponse(status=204)

	def get_studentpage(self, login):
		data = self.student_database.get_student(login)
		if data:
			return template('student', student=data)
		else:
			return HTTPResponse(status=204)