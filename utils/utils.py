from io import BytesIO
import base64
from PIL import Image
import requests
import json


def get_image_pil_from_string(base_string):
    buffer = BytesIO()
    buffer.write(base64.b64decode(base_string))
    buffer.seek(0)
    return Image.open(buffer)


def get_image_raw_from_string(base_string):
    buffer = BytesIO()
    buffer.write(base64.b64decode(base_string))
    buffer.seek(0)
    return buffer


def maxx(list):
    return max(list) if len(list) != 0 else 0


def get_result_from_microsoft_api(image):
    headers = {
        'Ocp-Apim-Subscription-Key': '31507b9626384f8ab2782fffcc11f0a3',
        'Content-Type': 'application/octet-stream'
    }
    req = requests.post('https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize',
                        headers=headers,
                        data=image)
    result = []
    rec_content = req.json()
    for i in rec_content:
        entity = {}
        entity['face_position'] = i["faceRectangle"]
        entity['emotion'] = max(i['scores'], key=i['scores'].get)
        result.append(entity)
    return result


def get_detection_score(pic_arr, address="localhost"):
    r = requests.post("http://" + address + ":4000/detection_scores/",
                      data=json.dumps({"64images": pic_arr}))
    return json.loads(r.content.decode())

def post_to_emotion_detection(pic_arr, address="localhost"):
    r = requests.post("http://" + address + ":5000/emotion_scores/",
                      data=json.dumps({"64images": pic_arr}))
    return json.loads(r.content.decode())
