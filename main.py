from intra import IntraAPIClient
import json
import sqlite3
from bottle import route, run, template
import re

ic = IntraAPIClient()

payload = {
   "filter[primary_campus]":13
}

def get_students_by_campus():
	ret_str = ''
	i_str = ''
	pattern = re.compile('3b3')
	response_list = ic.pages("campus/13/users")
	for i in response_list:
		i_str = (i['login'])
		if (pattern.search(i_str)):
			continue
		else:
			i_str += '<br>'
		ret_str += i_str
	return ret_str

def print_html():
	header_file = open('html_sources/header.txt')
	str1 = header_file.read()
	str2 = '<body>\n<div class="header">\n\t<h1>Evaluation reviewer</h1>\n</div>\n<div class="topnav">\n\t<a href="#">Link</a>\n\t<a href="#">Link</a>\n\t<a href="#">Link</a>\n\t<a href="#" style="float:right">Link</a>\n</div>\n<div class="row">\n\t<div class="leftcolumn">\n\t\t<div class="card">\n\t\t\t<h2>STUDENTS</h2>\n\t\t\t\t<h5>Hive Helsinki</h5>'
	str3 = get_students_by_campus()
	footer_file = open('html_sources/footer.txt')
	str4 = footer_file.read()
	return (str1 + str2 + str3 + str4)

html_str = print_html()

@route('/evals')
def evals():
	return html_str

run(host='localhost', port=8080, debug=True)
