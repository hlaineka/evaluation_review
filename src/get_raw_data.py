#helper to fetch data and go through it before reading it to the database

from intra import IntraAPIClient
import json
#from database import StudentDatabase

ic = IntraAPIClient()
#db = StudentDatabase()

file = open("data_test.json", "w")
#json_dump = file.read()
#data = json.loads(json_dump)
#student = db.get_student('hlaineka')
student_id = 61981
#print(student_id)
start = "2021-04-01"
end = "2021-04-25"
url = 'users/'+str(student_id)+'/scale_teams/as_corrector?range[begin_at]='+start+','+end
print(url)
response_list = ic.pages(url)
for i in (response_list):
    for w in i:
        print(w)
        print('\n')
file.write(json.dumps(response_list))
file.close()

