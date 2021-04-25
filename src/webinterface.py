import bottle
from bottle import route, run, template
from database import StudentDatabase

class WebInterface:
	def __init__ (self, studentdb):
		self.student_database = studentdb

	# gets all the students at Hive Helsinki
	def get_students(self):
		data = self.student_database.get_students()
		if data:
			html_insert = ''
			for student in data:
				html_insert += '<a href="/student/'+student[1]+'">'+student[1]+'</a>, <a href="'+student[2]+'">intra</a><br>'+'\n'
			return template('students', students=html_insert, style="styles.css")
		else:
			return HTTPResponse(status=204)

	def get_studentpage(self, login):
		data = self.student_database.get_student(login)
		if data:
			print ("data found")
			return template('student', student=data)
		else:
			return HTTPResponse(status=204)

	def get_start(self):
		unicorns = 'burpuni.gif'
		return template('start', picture=unicorns, style='styles.css')
	
	def get_index(self):
		return template('index', style="styles.css")

	def get_evals(self):
		evals = self.student_database.get_evals()
		html_insert = ''
		for data in evals:
				html_insert += '<a href="/eval/'+str(data[1])+'">'+str(data[1])+'</a><br>total_points: '+str(data[0])+'<br>time: '+data[3]+'<br>corrector: '+data[4]+'<br>correcteds: '+data[5]
				if data[6]:
					html_insert += ' '+data[6]
				if data[7]:
					html_insert += ' '+data[7]
				if data[8]:
					html_insert += ' '+data[8]
				html_insert += '<br><br>\n'
		if data:
			return template('evals', evals=html_insert, style="styles.css")
		else:
			return HTTPResponse(status=204)

	def get_eval(scale_id):
		one_eval = self.student_database.get_eval()
		html_insert += '<a href="/eval/'+str(data[1])+'">'+str(data[1])+'</a><br>total_points: '+str(data[0])+'<br>time: '+data[3]+'<br>corrector: '+data[4]+'<br>correcteds: '+data[5]
		if data[6]:
			html_insert += ' '+data[6]
		if data[7]:
			html_insert += ' '+data[7]
		if data[8]:
			html_insert += ' '+data[8]
		html_insert += '<br><br>\n'