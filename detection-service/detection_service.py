from flask import Flask, request
import json
from functional import seq
import dlib
import numpy as np
import sys
import os
from flask_cors import CORS
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
from utils.utils import maxx, get_image_pil_from_string

app = Flask(__name__)
CORS(app)
detector = dlib.get_frontal_face_detector()

@app.route('/detection_scores/', methods=['POST'])
def detection_scores():
    return json.dumps(list(seq(json.loads(request.data.decode('utf-8'))['64images']) \
                      .map(lambda x: np.array(get_image_pil_from_string(x)))\
                      .map(lambda x: maxx(detector.run(x, 1, -1)[1]))))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
