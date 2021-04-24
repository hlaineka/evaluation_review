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

@route('/wait.html')
def wait():
	unicorns = 'burpuni.gif'
	return template('wait', picture=unicorns)

@post('/wait.html')
def start_database():
	start = request.POST.get('start')
	print (start)
	if start:
		print("start is not None")
		studentdb.init_database()
		redirect('/index')

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

@route('/images/<picture>')
def serve_pictures(picture):
	return static_file(picture, root='images')

run(host='0.0.0.0', port=6660, debug=True)
