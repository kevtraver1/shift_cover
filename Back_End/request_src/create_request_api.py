import pdb
from flask import Flask, render_template,request
#from flask_ask import session
from flask_restful import Resource, Api
import boto3
from dynamodb_connection import Dynamodb_Connection



app = Flask(__name__)
app.secret_key = b'A\x8by\xbdl\xbcpj>.EfWo,\xf2'#CHANGE THIS LOOK INTO THIS
api = Api(app)



class Create_Request(Resource):
	def get(self):
		try:
			connection					= Dynamodb_Connection()
			data_hash 					= {}
			data_hash["description"]	= request.args.get('description', None)
			data_hash["start_time"]		= request.args.get('start_time', None)
			data_hash["end_time"]		= request.args.get('end_time', None)
			data_hash["date"]			= request.args.get('date', None)
			data_hash["account_id"]		= request.args.get('account_id', None)
			data_hash["username"]		= request.args.get('username', None)
			result						= connection.insert_item(data_hash)
		except Exception as e:
			result = "Fialed in api {}".format(e)
		return result

class Get_Request(Resource):
	def get(self):
		try:
			connection 	= Dynamodb_Connection()
			data_hash 					= {}
			data_hash["start_time"]		= request.args.get('start_time', None)
			data_hash["date"]			= request.args.get('date', None)
			result 						= connection.get_item(data_hash)
		except Exception as e:
			result = "Failed to get request becasue of {}".format(e)
		return result
class Delete_Request(Resource):
	def get(self):
		try:
			connection = Dynamodb_Connection()
			data_hash 					= {}
			data_hash["start_time"]		= request.args.get('start_time', None)
			data_hash["date"]			= request.args.get('date', None)
			result 						= connection.delete_item(data_hash)
		except Exception as e:
			result = "Failed to get request becasue of {}".format(e)
		return result		
class Connection_Test(Resource):
	def get(self):
		return {"TEST":"HELLO WORLD HERE I COME!!!"}


api.add_resource(Connection_Test,'/')
api.add_resource(Create_Request,'/Create_Request')
api.add_resource(Get_Request,'/Get_Request')
api.add_resource(Delete_Request,'/Delete_Request')

#https://ql8mgda8bl.execute-api.us-east-1.amazonaws.com/create_request_dev/Delete_Request?date=2018-11-10&start_time=10:00
##https://ql8mgda8bl.execute-api.us-east-1.amazonaws.com/create_request_dev/Create_Request?date=2018-11-10&start_time=10:00&end_time=17:00&description=blue muffin&account_id=1&username=ktraver1

if __name__=="__main__":
	app.run()