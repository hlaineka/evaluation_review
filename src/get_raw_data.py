#helper to fetch data and go through it before reading it to the database

from intra import IntraAPIClient
import json
from database import StudentDatabase

ic = IntraAPIClient()
#db = StudentDatabase()

file = open("data.json", "w")
json_dump = file.read()
data = json.loads(json_dump)
#student = db.get_student('hlaineka')
#student_id = student[0]
print(student_id)
url = "users/"+str(student_id)+"/scale_teams/as_corrector"
response_list = ic.get("teams/3534176/teams_uploads")
data = response_list.json()
for i in (data):
    print(i)
    print('\n')
file.close()
