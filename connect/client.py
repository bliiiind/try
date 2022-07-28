import requests

json_data = {'a': 1, 'b': 2}

r = requests.post("http://172.26.69.194:80/api/uwbget", json=json_data)

print(r.headers)
print(r.text)
