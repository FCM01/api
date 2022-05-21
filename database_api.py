
from cmath import pi
from ctypes.wintypes import PINT
from http import client
from lib2to3.pgen2 import token
from tokenize import group
from urllib import request
from flask import Flask, request, json, jsonify,render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson import json_util
from flask_cors import CORS
import json


app=Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/Hermes"
def parse_json(data):
    return json.loads(json_util.dumps(data))

mongo  = PyMongo(app)
CORS(app)
# signup and login functions below 
@app.route("/User/signup",methods=["POST"])
def signup():
    status = 200
    resp  ={}
    try:
        data = request.get_json("data")
        print(data)
        username = data["data"]["username"]
        email = data["data"]["email"]
        password = data["data"]["password"]
        database_check = mongo.db.user.find_one({"username":f"{username}","email":f"{email}"})
        print(parse_json(database_check))
        if parse_json(database_check) == None:
            if username != "" and email !="" and password != "":

                payload = {
                    "username":username ,
                    "email":email,
                    "password":password
                }
                mongo.db.user.insert_one(payload) 
                status = 200  
                resp = {"message":"user made", "token":"0"}
        else:
            print("we being used ")
            status = 200
            resp ={"message":"User credentials are in use","token":"1"}
        return jsonify(resp),status 
    except Exception as e  :
        print("ERROR on /User/signup",e)
        return jsonify(resp), status
@app.route("/Retrieve/Users",methods=["GET"])
def retrieve_users():
    status =200
    resp = {}
    try:
        database_check  = parse_json (mongo.db.user.find())
        print(database_check)
        array_users = []
        for database_chk in database_check:
            array_users.append(database_chk["username"])
        return jsonify(array_users)
    
    except Exception as e:
        print("ERROR on /User/Login",e)
        return jsonify(resp), status

@app.route("/User/Login",methods=["POST"])
def login():
    status =200
    resp = {}
    try:
        data = request.get_json("data")
        print(data)
        username = data["data"]["username"]
        password = data["data"]["password"]
        if username != "" and password != "":
            database_check  = mongo.db.user.find_one({"username":f"{username}"})
            print(parse_json(database_check))
            if parse_json(database_check) != None:

                database_password  = database_check["password"]
                if password == database_password:
                    data= parse_json(database_check)
                    resp ={"message":"success","user":data,"token":"0"}
                else:
                    status =200
                    resp  ={"message":"User password is incorrect","token":"1"}
            else :
                status = 200
                resp = {"message":"User does not exsit","token":"1"}
        return jsonify(resp),status
    except Exception as e:
        print("ERROR on /User/Login",e)
        return jsonify(resp), status

@app.route("/Make/group_chat",methods=["POST"])
def make_groupchat():
    status  = 200
    resp = {}
    try:
        data = request.get_json("data")
        print(data)
        group_name = data["data"]["group_name"]
        member_array = data ["data"]["member_array"]
        if group_name != "" and member_array != []:
            database_check  = mongo.db.chats.find({"group_name":f"{group_name}"})
            print(parse_json(database_check))
            if parse_json(database_check) == []:
                payload ={
                    "group_name":group_name,
                    "member_array":member_array
                }
                mongo.db.group_chats.insert_one(payload)
                resp = {"messge":"chat created"}
                return jsonify(resp),status
            else :
                status =300
                resp = {"message":"group name has been taken"}
        return jsonify(resp),status
    except Exception as e :
        print("ERROR on /Make/group_chat",e)
        return jsonify(resp),status


# making chat tye area below
@app.route("/Retrive/Memberships",methods =["POST"])
def retrieve_meberships():
    status  = 200
    resp = {}
    try:
        data = request.get_json("data")
        username = data["data"]["username"]
        print(username)
        database_check  = parse_json (mongo.db.group_chats.find())
        print(database_check)
        array_of_meberships = []
        for i in database_check:
            for j in i["member_array"]:
                if j == username:
                    array_of_meberships.append(i["group_name"])

        print(array_of_meberships)
        resp = {"memberships":array_of_meberships} 
        return jsonify(resp),status
    except Exception as e :
        print("ERROR on /Retrive/Memberships",e)
        return jsonify(resp),status

# idividual chat functions
@app.route("/Make/individual_chat",methods=["POST"])
def make_individualchat():
    status  = 200
    resp = {}
    try:
        data = request.get_json("data")
        print(data)
        user1 = data["data"]["user1"]
        user2 = data["data"]["user2"]
        room_id = data["data"]["room_id"]
        

        if  user1!= "" and user2  != "" and room_id !="":
            database_check  = mongo.db.chats.find({"user1":f"{room_id}","user2": f"{user2}"})
            database_check2  = mongo.db.chats.find({"user2":f"{room_id}","user1": f"{user2}"})
            print(parse_json(database_check))
            if parse_json(database_check) == [] and parse_json(database_check2)== []:
                payload ={
                    "user1":f"{user1}",
                    "user2": f"{user2}",
                    "room_id":f"{room_id}",
                }
                mongo.db.chats.insert_one(payload)
                resp = {"messge":"chat created"}
                return jsonify(resp),status
            else :
                status =300
                resp = {"message":"chat has already been made"}
        return jsonify(resp),status
    except Exception as e :
        print("ERROR on /Make/group_chat",e)
        return jsonify(resp),status


# making chat tye area below
@app.route("/Retrive/Chats",methods =["POST"])
def retrieve_chat():
    status  = 200
    resp = {}
    try:
        data = request.get_json("data")
        username = data["data"]["username"]
        database_check  = parse_json (mongo.db.chats.find())
        if parse_json(database_check) != []:
            chats =[]
            for i in parse_json(database_check):
                if i["user1"] == username:
                    payload ={
                        "user":i["user2"],
                        "room_id":i["room_id"]
                    }
                    chats.append(payload)
                if i["user2"] == username:
                    payload ={
                        "user":i["user1"],
                        "room_id":i["room_id"]
                    }
                    chats.append(payload)
            print("chats array=>",chats)
            resp = {"chats":chats} 
        return jsonify(resp),status
    except Exception as e :
        print("ERROR on /Retrive/Memberships",e)
        return jsonify(resp),status

@app.route("/Delete/Chat",methods= ["POST"])
def delete_chat():
    status = 200
    resp = {}
    try:
        data = request.get_json("data")
        room_id=data["data"]["room_id"]
        if room_id != "":
            database  = mongo.db.chats.find_one({"room_id":f"{room_id}"})
            if database != []:
                    mongo.db.chats.delete_one({"room_id":f"{room_id}"})
                    status =200
                    resp = {"message":"Chat has been deleted","status":status}
            else:
                status =400
                resp = {"message":"Chat not in database ","status":status}

    except Exception as e :
        status  = 400
        resp={"message":f"{e}","status":status}  
        print("ERORR (/Delete/Chat route)--->",e)
    return jsonify(resp),status

@app.route("/Delete/Groupchat",methods= ["POST"])
def delete_groupchat():
    status = 200
    resp = {}
    try:
        data = request.get_json("data")
        print(data)
        group_name =data["data"]["group_name"]
        if group_name  != "":
            database  = mongo.db.group_chats.find_one({"group_name":f"{group_name}"})
            if database != []:
                    mongo.db.group_chats.delete_one({"group_name":f"{group_name}"})
                    status =200
                    resp = {"message":"Group chat has been deleted","status":status}
            else:
                status =400
                resp = {"message":"Group chat not in database ","status":status}

    except Exception as e :
        status  = 400
        resp={"message":f"{e}","status":status}  
        print("ERORR (/Delete/Chat route)--->",e)
    return jsonify(resp),status
if __name__  =="__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0',port=5000)