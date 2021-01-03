import sys
import os
from flask import Flask, jsonify, request, flash
# from werkzeug.utils import secure_filename
# from segmenting_cycles import runSingleFile
import random
import string
import datetime
import math

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'i am here'


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    route = 'testing/'+file.filename
    file.save(route)
    # result = runSingleFile(route)
    # if result:
    #     result = "result is {}, accuracy = {}%".format(result[0], math.ceil(result[1]*100))
    # print(result)
    # return result
    return 'file sent to server'




def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str





if __name__ == "__main__":
   app.run(host='192.168.1.7', port=5000, debug=True)

