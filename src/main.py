import bottle
from bottle import route, run, template, redirect, abort, post, request
from webinterface import WebInterface
from database import StudentDatabase
import os
import requests

app = bottle.app()
studentdb = StudentDatabase()
web = WebInterface(studentdb)
user = ''

@route('/')
def index():
	html_str = web.get_index()
	return html_str

@route('/student/<login>')
def student(login):
	html_str = web.get_studentpage(login)
	return html_str

run(host='0.0.0.0', port=6660, debug=True)
