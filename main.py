import sys
import os
from flask import Flask, jsonify, request, flash
from werkzeug.utils import secure_filename
# from segmenting_cycles import segment,predict
import random
import string
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'i am here'


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    route = 'testing/'+file.filename
    file.save(route)

    # allMoves = segment(route)
    # print("number of moves = ", len(allMoves))
    # result = predict(allMoves)
    # print(result)
    return "jjjjjjjjjj"
    # return 'file sent to server'




def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str





if __name__ == "__main__":
   app.run(host='192.168.1.8', port=5000, debug=True)

