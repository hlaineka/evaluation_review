import bottle
from bottle import route, run, template
from database import StudentDatabase

# Class to create webpages to bottle from templates. Templates are saved in ./views
class WebInterface:
	def __init__ (self, studentdb):
		self.student_database = studentdb
		self.page_number = 0

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


	# get the page of a single student
	def get_studentpage(self, login):
		data = self.student_database.get_student(login)
		if data:
			return template('student', student=data)
		else:
			return HTTPResponse(status=204)

	#the landing page
	def get_start(self):
		unicorns = 'burpuni.gif'
		return template('start', picture=unicorns, style='styles.css')
	
	#front page after database has been created
	def get_index(self):
		return template('index', style="styles.css")

	#page listing all the evaluations
	def get_evals(self, start=None, end=None, page=1):
		start_index = (int(page) - 1) * 20
		evals = self.student_database.get_evals(start=start_index, start_date=start, end_date=end)
		html_insert = ''
		if not evals:
			return (template('evals', evals=html_insert, style="styles.css"))
		date_str = ''
		if (start and end):
			date_str = "&eval_start="+start+"&eval_end="+end
		if (int(page) > 1):
			html_insert += '<a href="/evals?page='+str(int(page) - 1)+date_str+'">prev   </a>'
		if evals:
			html_insert += '<a href="/evals?page='+str(int(page) + 1)+date_str+'">   next</a><br><br>'
		for data in evals:
				html_insert += '<a href="/eval/'+str(data[1])+'">'+str(data[1])+'</a><br>total_points: '+str(data[0])+'<br>time: '+data[3]+'<br>corrector: '+data[4]+'<br>correcteds: '+data[5]
				if data[6]:
					html_insert += ' '+data[6]
				if data[7]:
					html_insert += ' '+data[7]
				if data[8]:
					html_insert += ' '+data[8]
				html_insert += '<br><br>\n'
		return template('evals', evals=html_insert, style="styles.css")

	#page for single eval with more information
	def get_eval(self, scale_id):
		one_eval = self.student_database.get_eval(scale_id)
		project_name = self.student_database.get_project_name(one_eval[3])
		correcteds = one_eval[9]
		if one_eval[10]:
			correcteds += ', '+one_eval[10]
		if one_eval[11]:
			correcteds += ', '+one_eval[11]
		if one_eval[12]:
			correcteds += ', '+one_eval[12]
		corrector = one_eval[0]
		comment = one_eval[4]
		comment_points = one_eval[5]
		final_mark = one_eval[6]
		final_mark_points = one_eval[7]
		begin_at = one_eval[8]
		duration = one_eval[14]
		duration_points = one_eval[15]
		feedback_comment = one_eval[17]
		feedback_rating = one_eval[18]
		feedback_points = one_eval[19]
		return template('eval', one_eval=one_eval, project_name=project_name, corrector=corrector, correcteds=correcteds, style="styles.css", comment=comment, comment_points=comment_points, final_mark=final_mark, final_mark_points=final_mark_points, begin_at = begin_at, duration=duration, duration_points=duration_points, feedback_comment=feedback_comment, feedback_rating=feedback_rating, feedback_points=feedback_points)

	def get_search(self, errorstr=''):
		return(template('search', style="styles.css", errorstr=errorstr))