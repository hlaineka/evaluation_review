from intra import IntraAPIClient
import json

ic = IntraAPIClient()

file = open("data.json", "w")
response_list = ic.pages("campus/13/users")
json.dump(response_list, file)
file.close()
