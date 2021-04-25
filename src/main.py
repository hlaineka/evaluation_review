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
	studentdb.init_database()
	redirect("/index")

@route('/index')
def index():
	html_str = web.get_index()
	return html_str

@route('/students')
def students():
	html_str = web.get_students()
	return html_str

@route('/evals')
def evals():
	html_str = web.get_evals()
	return html_str

@route('/student/<login>')
def student(login):
	html_str = web.get_studentpage(login)
	return html_str

@route('/images/<picture>')
def serve_pictures(picture):
	return static_file(picture, root='images')

@route('/static/<filename>')
def send_static(filename):
	return static_file(filename, root='./static/')

run(host='0.0.0.0', port=6660, debug=True)
