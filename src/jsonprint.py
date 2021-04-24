#helper to go through fetched data before adding it to the database

import json

file = open('data_cursus.json')
json_dump = file.read()
data = json.loads(json_dump)
for i in data:
	for w in i:
		for j in (w['campus']):
			if (j['id'] == 13):
				print (w['name'])
				print (w['cursus'])
				print (w['id'])
				print (w['slug'])
				print('\n')
