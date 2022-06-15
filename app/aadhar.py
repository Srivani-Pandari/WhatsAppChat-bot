from app import app
from flask import Flask, request, jsonify
import json

data = [{"uid": "709260738705", "name": "Narahari"},
        {"uid": "123456789012", "name": "Naveen"}]


@app.route("/generateOTPForOAuth", methods=['POST'])
def uid():
    body = json.loads(request.data)
    print(body['uid'])
    if(body['uid'].isnumeric()):
        return jsonify({"message": "success"})
    else:
        return jsonify({"message": "failure"}), 400


@app.route("/getAdharDetailsByUid/<uid>", methods=['GET'])
def getCall(uid):
    for eachObject in data:
        if eachObject['uid'] == uid:
            return jsonify(eachObject)

    return jsonify({"error": "not found with uid "+uid}), 400


@app.route("/getAdharDetailsByUid", methods=['GET'])
def getRequestParameters():
    uid = request.args.get('uid', None)
    name = request.args.get('name', None)
    print(uid)
    print(name)
    if(uid != None):
        resp = check(data, 'uid', uid)
        return jsonify(resp)
    elif(name != None):
        resp = check(data, 'name', name)
        if(resp != None):
            return jsonify(resp)

        return jsonify({"error": "not found with "+name}), 400
    else:
        return jsonify({"error": "Something went"}), 500

    return jsonify({"error": "not found with "}), 400


def check(data, key, value):

    for eachObject in data:
        if eachObject[key] == value:
            return eachObject
    return None
