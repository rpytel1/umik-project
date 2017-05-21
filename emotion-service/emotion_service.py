from flask import Flask, request
import json
from functional import seq
import requests
import sys
import os
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
from utils.utils import get_image_from_string, get_result_from_microsoft_api
from pymongo import MongoClient
from bson.objectid import ObjectId
import copy
import time
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
mongo_client = MongoClient()["emotion_faces"]["emotion_entities"]


@app.route('/emotion_scores/', methods=['POST', 'GET'])
def emotion_scores():
    if request.method == 'POST':
        result = list(seq(json.loads(request.data.decode('utf-8'))['64images'])
                        .map(lambda x: get_image_from_string(x))
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


# @app.route('/emotion_scores/<object_id>/', methods=['GET'])
# def emotion_scores(object_id):
#     result = []
#     for entity in mongo_client.find({"_id": ObjectId(object_id)}):
#         result.append({entity["face_position"], entity["emotion"]})
#     return json.dumps(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
