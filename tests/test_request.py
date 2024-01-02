import requests
import json

r_json = requests.get("https://jsonplaceholder.typicode.com/todos").json()

# for todo_data in r_json:
#         print(todo_data)

print(r_json)
        