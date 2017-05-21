import requests
import json
import base64

b64 = base64.b64encode(open("../webpage-service/resources/img/arnie.jpg", "rb").read())
r = requests.post("http://localhost:5000/emotion_scores/", data=json.dumps({"64images": [b64.decode("utf-8")]}))
print (r.status_code)
print(r.content)