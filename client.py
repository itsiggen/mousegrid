import requests

r = requests.get("http://localhost:5000/alterego/result")
result = r.json();
print(result["success"]);
