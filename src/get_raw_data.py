from intra import IntraAPIClient
import json
from database import StudentDatabase

ic = IntraAPIClient()
db = StudentDatabase()

file = open("data.json", "w")
student = db.get_student('hlaineka')
student_id = student[0]
url = "users/"+str(student_id)+"/scale_teams/as_corrector"
response_list = ic.pages(url)
json.dump(response_list, file)
file.close()
