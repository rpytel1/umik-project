from flask import Flask, request
import json
from functional import seq
import dlib
import numpy as np
# from .. utils.utils import maxx, get_image_from_string
from io import BytesIO
import base64
from PIL import Image



def get_image_from_string(base_string):
    buffer = BytesIO()
    buffer.write(base64.b64decode(base_string))
    buffer.seek(0)
    return Image.open(buffer)

def maxx(list):
    return max(list) if len(list) != 0 else 0

app = Flask(__name__)
detector = dlib.get_frontal_face_detector()

@app.route('/detection_scores/', methods=['POST', 'GET'])
def detection_scores():
    return json.dumps(list(seq(json.loads(request.data.decode('utf-8'))['64images']) \
                      .map(lambda x: np.array(get_image_from_string(x)))\
                      .map(lambda x: maxx(detector.run(x, 1, -1)[1])))), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
