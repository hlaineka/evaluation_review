import sqlite3
from os import path
import json
import re
from intra import IntraAPIClient
from datetime import datetime	

timeformat = '%Y-%m-%dT%H:%M:%S.%fZ'

def	get_final_mark_points():
	return 0

def get_too_friendly_points():
		return 0

def get_duration_points(team):
		start_time = datetime.strptime(team['begin_at'], timeformat)
		end_time = datetime.strptime(team['filled_at'], timeformat)
		target_time = team['scale']['duration']
		minimum_time = target_time * 0.66
		duration = (end_time - start_time).total_seconds()
		duration_points = 0
		if duration < minimum_time:
			duration_points = -42
		elif duration < target_time:
			duration_points = -10
		elif duration > target_time * 1.5:
			duration_points = 20
		else:
			duration_points = 10
		return duration_points

def calculate_eval_points(scale_id, team):
		comment_len = len(team['comment'])
		if (comment_len > 180):
			comment_points = 1
			#self.database.execute("UPDATE scales SET comment_points = 1 WHERE scale_id = (?)", (scale_id, ))
		final_mark_points = get_final_mark_points()
		#self.database.execute("UPDATE scales SET final_mark_points ="+str(final_mark_points)+" WHERE scale_id = (?)", (scale_id, ))
		too_firendly_points = get_too_friendly_points()
		#self.database.execute("UPDATE scales SET too_friendly_points ="+str(too_friendly_points)+" WHERE scale_id = (?)", (scale_id, ))
		duration_points = get_duration_points(team)
		flags_points = 0
		feedback_total_points = 0
		#self.database.execute("UPDATE scales SET too_friendly_points ="+str(too_friendly_points)+" WHERE scale_id = (?)", (scale_id, ))
		total_points = comment_points + final_mark_points + too_firendly_points + duration_points + flags_points + feedback_total_points
		#self.database.commit()
		print(team['comment'])
		print(total_points)

def	save_scale_team(team):
		# checking that the evaluation did actually happen
		if not team['filled_at']:
			return
		scale_id = team['id']
		feedback_id = team['feedbacks'][0]['id']
		#cursor = self.database.cursor()
		#cursor.execute("INSERT INTO scales (corrector, id, scale_id, project_id, comment, final_mark, begin_at, filled_at, duration, feedback_comment, feedback_rating, feedback_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ('hlaineka', team['id'], team['scale_id'], team['team']['project_id'], team['comment'], team['final_mark'], team['begin_at'], team['filled_at'], team['scale']['duration'], team['feedbacks'][0]['comment'], team['feedbacks'][0]['rating'], team['feedbacks'][0]['id'] ))
		# detailed info on the feedback rating points
		#url = "feedbacks/"+str(feedback_id)
		#response = ic.get(url)
		#data = response.json()
		#feedback_points = 0
		#for i in (data['feedback_details']):
		#	feedback_points += i['rate']
		#executable = "UPDATE scales SET feedback_points = "+str(feedback_points)+" WHERE id = "+str(scale_id)
		#cursor.execute(executable)
		#i = 0
		# adding the correcteds
		#for person in team['correcteds']:
		#	if (i < 3):
				#executable = "UPDATE scales SET corrected"+str(i+1)+" = \""+person['login']+"\" WHERE id = "+str(scale_id)
		#		cursor.execute(executable)
		#	i += 1
		calculate_eval_points(scale_id, team)
		#self.database.commit()
		return
	
def save_student_teams():
		file = open('data.json')
		json_dump = file.read()
		data = json.loads(json_dump)
		for i in data:
			for w in i:
				save_scale_team(w)

save_student_teams()