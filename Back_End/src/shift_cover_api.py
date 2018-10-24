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
        response    = connection.account_login(username,password)
        return json.dumps(response, indent=4, sort_keys=True, default=str)
class Create_Account(Resource):
    def get(self):
        connection  = DB_Connection()
        username    = request.args.get('username', None)
        password    = request.args.get('password', None)
        company     = request.args.get('company', None)
        account_pic = request.args.get('account_pic', None)
        role        = request.args.get('role', None)
        response    = connection.create_account(username,password,company,role,account_pic)

        return json.dumps(response, indent=4, sort_keys=True, default=str)
class Update_Account(Resource):
    def get(self):
        connection  = DB_Connection()
        username    = request.args.get('username', None)
        password    = request.args.get('password', None)
        company     = request.args.get('company', None)
        account_pic = request.args.get('account_pic', None)
        role        = request.args.get('role', None)
        account_id  = request.args.get('account_id', None)
        response    = connection.update_account(username,password,company,role,account_pic,account_id)
        return json.dumps(response, indent=4, sort_keys=True, default=str)
class Delete_Account(Resource):
    def get(self):
        connection  = DB_Connection()
        account_id  = request.args.get('account_id', None)
        response    = connection.delete_account(account_id)
        return response     
class Get_Accounts(Resource):
    def get(self):
        connection  = DB_Connection()
        response    = connection.get_accounts()
        return json.dumps(response, indent=4, sort_keys=True, default=str)

class Get_Account(Resource):
    def get(self):
        connection  = DB_Connection()
        username    = request.args.get('username', None)
        response    = connection.get_account(username)
        return json.dumps(response, indent=4, sort_keys=True, default=str)
class Connection_Test(Resource):
    def get(self):
        return "HELLO WORLD HERE I COME!!!"

def create_output_hash(response):
    

api.add_resource(Connection_Test,'/') 
api.add_resource(Login,'/login')
api.add_resource(Create_Account,'/create_account')
api.add_resource(Update_Account,'/update_account')
api.add_resource(Delete_Account,'/delete_account')
api.add_resource(Get_Accounts,'/get_accounts')
api.add_resource(Get_Account,'/get_account')

if __name__=="__main__":
	app.run()
#http://127.0.0.1:5000/login?username=kevin&password=travers
#update_account?username=DELETEME&password=FAKEPASSWORD&company=cbs&role=VOD_system_ADMIN&account_pic=MY_FACE&account_id=4
#api created/ backend clean up
#rds create and connect
#local connection test
#docker github publish ec2 instance
#this weekend git portfilio 
#@app.route("/login")
#def login():
#   pass
