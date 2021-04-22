from intra import IntraAPIClient
import json
import sqlite3
from bottle import route, run, template

@route('/evals')

def evals():
    return "Hello world"

ic = IntraAPIClient()

payload = {
   "filter[primary_campus]":13
}

response = ic.get("scale_teams")
if response.status_code == 200:
	data = response.json()

for i in data:
	print (i['id'])

run(host='localhost', port=8080, debug=True)