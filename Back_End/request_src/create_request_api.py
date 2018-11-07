import pdb
from flask import Flask, render_template,request
#from flask_ask import session
from flask_restful import Resource, Api
import json
import boto3
from dynamodb_connection import dynamodb_connection



app = Flask(__name__)
app.secret_key = b'A\x8by\xbdl\xbcpj>.EfWo,\xf2'#CHANGE THIS LOOK INTO THIS
api = Api(app)


#make login company specifc
class Get_Row(Resource):
    def get(self):
        connection      = dynamodb_connection()
        username        = request.args.get('username', None)
        password        = request.args.get('password', None)
        #company     = request.args.get('company', None)
        response        = connection.account_login(username,password)
        return response#json.dumps(response, indent=4, sort_keys=True, default=str)
class Insert_Row(Resource):
    def get(self):
        connection      = dynamodb_connection()
        #LOOK INTO BETTER VERSION OF GETTING
        #OR CREATE FUNCTION TO PARSE DATA INTO HASH
        username        = request.args.get('username', None)
        password        = request.args.get('password', None)
        company         = request.args.get('company', None)
        account_picture = request.args.get('account_picture', None)
        occupation      = request.args.get('occupation', None)
        email           = request.args.get('email', None)
        first_name      = request.args.get('first_name', None)
        last_name       = request.args.get('last_name', None)
        response        = connection.create_account(username,password,company,occupation,email,first_name,last_name)
        return response#json.dumps(response, indent=4, sort_keys=True, default=str)
class Update_Row(Resource):
    def get(self):
        connection      = dynamodb_connection()
        username        = request.args.get('username', None)
        password        = request.args.get('password', None)
        company         = request.args.get('company', None)
        account_picture = request.args.get('account_picture', None)
        occupation      = request.args.get('occupation', None)
        email           = request.args.get('email', None)
        first_name      = request.args.get('first_name', None)
        last_name       = request.args.get('last_name', None)
        account_id      = request.args.get('account_id', None)
        response        = connection.update_account(username,password,company,occupation,email,first_name,last_name,account_picture,account_id)
        return response#json.dumps(response, indent=4, sort_keys=True, default=str)
class Delete_Row(Resource):
    def get(self):
        connection  = dynamodb_connection()
        account_id  = request.args.get('account_id', None)
        response    = connection.delete_account(account_id)
        #return treu of false if account was deleted play with deleting
        return response    
class Get_Rows(Resource):
    def get(self):
        connection      = dynamodb_connection()
        response        = connection.get_accounts()
        return response#json.dumps(response, indent=4, sort_keys=True, default=str)

class Get_Row_By_ID(Resource):
    def get(self):
        connection      = dynamodb_connection()
        username        = request.args.get('username', None)
        response        = connection.get_account(username)
        return response#json.dumps(response, indent=4, sort_keys=True, default=str)

class Connection_Test(Resource):
    def get(self):
        return "HELLO WORLD HERE I COME!!!"


api.add_resource(Connection_Test,'/') 
api.add_resource(Login,'/Get_Row')
api.add_resource(Create_Account,'/Insert_Row')
api.add_resource(Update_Account,'/Update_Row')
api.add_resource(Delete_Account,'/Delete_Row')
api.add_resource(Get_Accounts,'/Get_Rows')
api.add_resource(Get_Account,'/Get_Row_By_ID')
#JOB_TITLE is STILL the error change it to occupation

if __name__=="__main__":
	app.run()