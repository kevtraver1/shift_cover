import pdb
from flask import Flask, render_template,request
#from flask_ask import session
from flask_restful import Resource, Api
from DB_Connection import DB_Connection
import json
import boto3

app = Flask(__name__)
app.secret_key = b'A\x8by\xbdl\xbcpj>.EfWo,\xf2'
api = Api(app)


class Login(Resource):
    def get(self):
        connection  = DB_Connection()
        username    = request.args.get('username', None)
        password    = request.args.get('password', None)
        #company     = request.args.get('company', None)
        response    = connection.profile_login(username,password)
        return response
class Create_Account(Resource):
    def get(self):
        connection  = DB_Connection()
        username    = request.args.get('username', None)
        password    = request.args.get('password', None)
        company     = request.args.get('company', None)
        profile_pic = request.args.get('profile_pic', None)
        role       = request.args.get('role', None)
        response    = connection.create_profile(username,password,company,role,profile_pic)
        return response        
class Update_Profile(Resource):
    def get(self):
        connection  = DB_Connection()
        username    = request.args.get('username', None)
        password    = request.args.get('password', None)
        company     = request.args.get('company', None)
        profile_pic = request.args.get('profile_pic', None)
        role       = request.args.get('role', None)
        response    = connection.update_profile(username,password,company,role,profile_pic)
        return response
class Delete_Profile(Resource):
    def get(self):
        connection  = DB_Connection()
        profile_id    = request.args.get('profile_id', None)
        response    = connection.create_profile(profile_id)
        return response     
class Get_Profiles(Resource):
    def get(self):
        connection  = DB_Connection()
        response    = connection.get_profiles()
        return json.dumps(response, indent=4, sort_keys=True, default=str)

class Get_Profile(Resource):
    def get(self):
        connection  = DB_Connection()
        username  = request.args.get('username', None)
        response    = connection.get_profile(username)
        return response 
api.add_resource(Login,'/login')
api.add_resource(Create_Account,'/create_account')
api.add_resource(Update_Profile,'/update_profile')
api.add_resource(Delete_Profile,'/delete_profile')
api.add_resource(Get_Profiles,'/get_profiles')
api.add_resource(Get_Profile,'/get_profile')

if __name__=="__main__":
	app.run()
#http://127.0.0.1:5000/login?username=kevin&password=travers
#api created/ backend clean up
#rds create and connect
#local connection test
#docker github publish ec2 instance
#this weekend git portfilio 
#@app.route("/login")
#def login():
#   pass
