import os
from os.path import isfile, join
from os import listdir
from flask import Flask, jsonify, request, flash
# from LSTM_ALI import pred_lstm
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'i am here'

# http://192.168.1.8:5000/upload
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    route = 'beso/'+file.filename
    file.save(route)
    return 'file sent to server'

# http://192.168.1.8:5000/ali
@app.route('/feeds', methods=['POST'])
def uploadFiles():
    gyroscope_file = request.files['sensorsFiles0']
    accelerometer_file = request.files['sensorsFiles1']
    dir = "dataset/u2/walking"
    # dirs = [f for f in listdir(dir) if isfile(join(dir, f))]
    dirs = os.listdir(dir)
    print(len(dirs), type(dirs))
    print(dirs)
    if len(dirs) >0:

        dirs = list(map(int, dirs))
        dirs.sort()
        print("max",max(dirs))
        new  = max(dirs) + 1
    else:
        new = 1

    dir = "dataset/u2/walking/"+str(new)
    print(dir)
    os.mkdir(dir)
    gFileRoute = dir + "/g" + str(new) + ".txt"
    aFileRoute = dir + "/a" + str(new) + ".txt"
    gyroscope_file.save(gFileRoute)
    accelerometer_file.save(aFileRoute)
    return "result"




if __name__ == "__main__":
   app.run(host='192.168.1.8', port=5000, debug=True)


