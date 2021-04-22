from intra import IntraAPIClient
import json
import bottle
from bottle import route, run, template
import re
from database import StudentDatabase

app = bottle.app()

ic = IntraAPIClient()

student_database = StudentDatabase('students.db')

payload = {
   "filter[primary_campus]":13
}

def save_students():
	pattern = re.compile('3b3')
	file = open('data.json')
	json_dump = file.read()
	response_list = json.loads(json_dump)
	for i in response_list:
		for w in i:
			try:
				if (pattern.search(w['login'])):
					continue
				else:
					student_database.save_student(w)
			except TypeError:
				break

# gets all the students at Hive Helsinki
def get_students_by_campus():
	ret_str = ''
	i_str = ''
	students = student_database.get_students()
	for i in students:
		i_str = str(i[0])
		i_str += ", "
		i_str += i[1]
		i_str += ", "
		i_str += i[2]
		i_str += "<br>\n"
		ret_str += i_str
	return ret_str

# returns the html required by bottle to create the main page
def get_html():
	header_file = open('src/html_sources/header.txt')
	str1 = header_file.read()
	str2 = '<body>\n<div class="header">\n\t<h1>Evaluation reviewer</h1>\n</div>\n<div class="topnav">\n\t<a href="#">Link</a>\n\t<a href="#">Link</a>\n\t<a href="#">Link</a>\n\t<a href="#" style="float:right">Link</a>\n</div>\n<div class="row">\n\t<div class="leftcolumn">\n\t\t<div class="card">\n\t\t\t<h2>STUDENTS</h2>\n\t\t\t\t<h5>Hive Helsinki</h5>'
	str3 = get_students_by_campus()
	footer_file = open('src/html_sources/footer.txt')
	str4 = footer_file.read()
	return (str1 + str2 + str3 + str4)

if not (student_database.students_added()):
	save_students()

html_str = get_html()

@route('/evals')
def evals():
	return html_str

run(host='0.0.0.0', port=8080, debug=True)
