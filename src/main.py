import bottle
from bottle import route, run, template, redirect, abort, post, request, static_file
from webinterface import WebInterface
from database import StudentDatabase
import os
import requests
import time

app = bottle.app()
studentdb = StudentDatabase()
web = WebInterface(studentdb)
user = ''

@route('/')
def start():
	html_str = web.get_start()
	return html_str

@post('/')
def redirect_to_wait():
	button = request.forms.get('start')
	if button:
		redirect('/wait')

@route('/wait')
def wait():
	start = request.query.start or None
	end = request.query.start or None
	studentdb.init_database(start, end)
	redirect("/index")

@route('/index')
def index():
	html_str = web.get_index()
	return html_str

@route('/students')
def students():
	html_str = web.get_students()
	return html_str

@route('/student/<login>')
def student(login):
	html_str = web.get_studentpage(login)
	return html_str

@route('/evals')
def evals():
	page = request.query.page or 1
	start = request.query.get('eval_start') or None
	end = request.query.get('eval_end') or None
	html_str = web.get_evals(page=page, start=start, end=end)
	return html_str


@route('/eval/<eval_id>')
def student(eval_id):
	html_str = web.get_eval(eval_id)
	return html_str

@route('/search')
def search():
	search_get = request.query.decode()
	eval_start = search_get.get('eval_start')
	eval_end = search_get.get('eval_end')
	errorstr = ''
	if eval_start and eval_end:
		redirect("/evals?eval_start="+eval_start+"&eval_end="+eval_end)
	if eval_start or eval_end:
		errorstr = "Select start and end date"
	html_str = web.get_search(errorstr)
	return html_str

@route('/images/<picture>')
def serve_pictures(picture):
	return static_file(picture, root='images')

@route('/static/<filename>')
def send_static(filename):
	return static_file(filename, root='./static/')

run(host='0.0.0.0', port=6660, debug=True)
