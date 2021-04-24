#helper to fetch data and go through it before reading it to the database

from intra import IntraAPIClient
import json
from database import StudentDatabase

ic = IntraAPIClient()
db = StudentDatabase()

file = open("data_cursus.json", "w")
student = db.get_student('hlaineka')
student_id = student[0]
url = "users/"+str(student_id)+"/scale_teams/as_corrector"
response_list = ic.pages("cursus/1/projects")
for i in response_list:
   print(i)
json.dump(response_list, file)
file.close()
