import json
import socket
from flask import Flask, jsonify, request, flash
from DatabaseConnection import getResults, addRow, signup

IPv4 = socket.gethostbyname(socket.gethostname())
app = Flask(__name__)

@app.route('/getTeamPerformanceDetails', methods=['POST'])
def getTeamPerformanceDetails():
    query = f'SELECT `id`, `moveId`, `totalCorrectMoves`, `totalwrongMoves`, `totalDuration`, `performancePercentage`, `teamPerformanceId` FROM `teamperformancedetails` WHERE `isdeleted` = 0'
    # print("query",query)
    performances = getResults(query)
    data = {}
    for tpd in performances:
        data.update({"teamPerformanceDetails": {"id": tpd[0],
                                                "moveId": tpd[1],
                                                "totalCorrectMoves": tpd[2],
                                                "totalwrongMoves": tpd[3],
                                                "totalDuration": tpd[4],
                                                "performancePercentage": tpd[5],
                                                "teamPerformanceId": tpd[6]}})
        data.update({"teamPerformanceDetails1": {"id": tpd[0],
                                                "moveId": tpd[1],
                                                "totalCorrectMoves": tpd[2],
                                                "totalwrongMoves": tpd[3],
                                                "totalDuration": tpd[4],
                                                "performancePercentage": tpd[5],
                                                "teamPerformanceId": tpd[6]}})

    print("teamPerformanceDetails=",data)
    jsonify(data)
    return json.dumps(data)


@app.route('/signIn', methods=['POST'])
def signIn():
    model = request.json
    email = model["email"]
    password = model["password"]
    query = f'SELECT * FROM `user` WHERE email = "{email}" AND password = "{password}" AND isdeleted = 0;'
    # print("query",query)
    user = getResults(query)[0]
    user = {"id": user[0], "name": user[1], "userTypeId": user[2], "email": user[3], "password": user[3], "isVerified": user[5]}
    # print("user=",user)
    jsonify(user)
    return json.dumps(user)

@app.route('/signUp', methods=['POST'])
def signUp():
    model = request.json
    tableName = model["modelName"]
    filter(model)
    cols = get_ColNames(model.keys())
    values = get_Values(model)
    query = f"INSERT INTO `{tableName}`({cols}) VALUES ({values}) "
    # print("query",query)
    id = signup(query, model["email"])
    return json.dumps(id)

@app.route('/insert', methods=['POST'])
def addUser():
    model = request.json
    tableName = model["modelName"]
    filter(model)
    cols = get_ColNames(model.keys())
    values = get_Values(model)
    query = f"INSERT INTO `{tableName}`({cols}) VALUES ({values}) "
    # print("query",query)
    cursor = addRow(query)
    id = cursor.lastrowid if cursor.rowcount == 1 else 0
    return json.dumps(id)


def filter(model):
    model.pop("modelName")
    model.pop("id")
    if "isdeleted" in model:
        model.pop("isdeleted")
    if "createdat" in model:
        model.pop("createdat")
    if "updatedat" in model:
        model.pop("updatedat")


@app.route('/getUser', methods=['POST'])
def uploaddb():
    id = request.args.get("id")
    print("id",id)
    query = "SELECT * FROM me WHERE id = {}; ".format(2)
    print(query)
    results = getResults(query)
    print("results",results[0])
    jsonify1 = jsonify(results[0])
    user = {"id":2,"name":"mohamed"}
    print("jsonify1=",jsonify(user))
    return json.dumps(user)


# @app.route('/getUser', methods=['POST'])
# def getuser():
#     print("type =",type(request))
#     print("value =",request)
#     return request.json

def get_ColNames(cols):
    sum = ""
    for col in cols:
        sum += f"`{col}`,"
    sum = sum[:-1]
    return sum

def get_Values(cols):
    sum = ""
    for col in cols:
        sum += f"'{cols[col]}'," if isinstance(cols[col], str) else f"{cols[col]},"
    sum = sum[:-1]
    return sum



if __name__ == "__main__":
   app.run(host=IPv4, port=5000, debug=True)


