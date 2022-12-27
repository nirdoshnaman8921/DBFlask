from flask import Flask,request,jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['MONGO_URI'] = "mongodb://localhost:27017/data"

mongo = PyMongo(app)


@app.route('/add-emp',methods=['POST'])
def add():
    name = request.json['name']
    pwd = request.json['pass']
    if name and pwd and request.method=="POST":
        id = mongo.db.emp.insert_one({'name':name,'pass':pwd})
        resp = "User added Succesfully"
        return jsonify(resp)

    else:
        return not_found()
    
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':"Not Found" + request.url
    }
    resp = jsonify(message)
    return resp

@app.route('/all-emp',methods=['GET'])
def show():
    users = mongo.db.emp.find()
    resp = dumps(users)
    return resp


@app.route('/show-emp/<id>',methods=['GET'])
def show_one(id):
    users = mongo.db.emp.find_one({'_id':ObjectId(id)})
    resp = dumps(users)
    return resp

@app.route('/dlt-emp/<id>',methods=['DELETE'])
def dlt_one(id):
    mongo.db.emp.delete_one({'_id':ObjectId(id)})
    resp = "User deleted Succesfully"
    return jsonify(resp)

@app.route('/update-emp/<id>',methods=['PUT'])
def update(id):
    name = request.json['name']
    pwd = request.json['pass']
    mongo.db.emp.update_one({'_id':ObjectId(id)},{'$set':{'name':name,'pass':pwd}})
    resp = "User updated Succesfully"
    return jsonify(resp)

if __name__ == "__main__":
    app.run()