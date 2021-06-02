import requests

url = "http://localhost:5000/api/people"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.json())
print(response.headers)
print(response.text)