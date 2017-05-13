from flask import Flask, request
import json
from functional import seq
import requests
# from ..utils.utils import get_image_from_string
from io import BytesIO
import base64
from PIL import Image
from pymongo import MongoClient
from bson.objectid import ObjectId
import copy
import time

def get_image_from_string(base_string):
    buffer = BytesIO()
    buffer.write(base64.b64decode(base_string))
    buffer.seek(0)
    return buffer

def maxx(list):
    return max(list) if len(list) != 0 else 0

app = Flask(__name__)
mongo_client = MongoClient()["emotion_faces"]["emotion_entities"]

def get_result_from_microsoft_api(image):
    headers = {
        'Ocp-Apim-Subscription-Key': '31507b9626384f8ab2782fffcc11f0a3',
        'Content-Type': 'application/octet-stream'
    }
    req = requests.post('https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize',
                        headers=headers, data=image)
    print(req.content)
    result = []
    rec_content = req.json()
    for i in rec_content:
        entity = {}
        entity['face_position'] = i["faceRectangle"]
        entity['emotion'] = max(i['scores'], key=i['scores'].get)
        result.append(entity)
    return result


@app.route('/emotion_scores/', methods=['POST', 'GET'])
def emotion_scores():
    if request.method == 'POST':
        result = list(seq(json.loads(request.data.decode('utf-8'))['64images']) \
                        .map(lambda x: get_image_from_string(x)) \
                        .map(lambda x: get_result_from_microsoft_api(x)))

        copy_res = copy.deepcopy(result)
        for entities in copy_res:
            for entity in entities:
                entity["time"] = time.time()
                entity["picture"] = json.loads(request.data.decode('utf-8'))['64images']
                mongo_client.insert(entity)
                mongo_client.save(entity)

        return json.dumps(result)

    else:
        result = []
        for entity in mongo_client.find({}):
            result.append({"face_position": entity["face_position"],
                           "emotion": entity["emotion"],
                           "time": entity["time"],
                           "picture": entity["picture"]})
        return json.dumps(result)


@app.route('/emotion_scores/<object_id>/', methods=['GET'])
def detection_scores(object_id):
    result = []
    for entity in mongo_client.find({"_id": ObjectId(object_id)}):
        result.append({entity["face_position"], entity["emotion"]})
    return json.dumps(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
