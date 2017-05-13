from io import StringIO
from flask import Flask, request
import json
from functional import seq
import dlib
import base64
import numpy as np
from PIL import Image

app = Flask(__name__)
detector = dlib.get_frontal_face_detector()


@app.route('/detection_scores/', methods=['POST'])
def hello_world():
    return json.dumps(seq(json.load(request.data('64images'))) \
                      .map(lambda x: np.asarray(Image.open(StringIO().write(base64.b64decode(x)))))\
                      .map(lambda x: max(detector.run(x, 1, -1)[1])))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
