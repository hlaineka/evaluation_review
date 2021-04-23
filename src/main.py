import bottle
from bottle import route, run, template, redirect, abort, post, request
from html_create import WebInterface
import os
import requests

app = bottle.app()
web = WebInterface()
user = ''

@route('/')
def index():
	html_str = web.get_index()
	return html_str

run(host='0.0.0.0', port=6660, debug=True)
