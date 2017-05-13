import os
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/detection_score/', methods=['GET'])
def hello_world():
    request.args.get('64image')
    #TODO
    return json.dump({"score": 0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

