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
			result = "NOTHING"

			#data_hash 					= "Dictionary"
			#data_hash["description"]	= request.args.get('description', None)
			#data_hash["start_time"]		= request.args.get('start_time', None)
			#data_hash["end_time"]		= request.args.get('end_time', None)
			#data_hash["date"]			= request.args.get('date', None)
			#data_hash["account_id"]		= request.args.get('account_id', None)
			result					= connection.insert_row()
		except Exception as e:
			result = "Fialed in api {}".format(e)
		return result

class Connection_Test(Resource):
	def get(self):
		return "HELLO WORLD HERE I COME!!!"


api.add_resource(Connection_Test,'/')
api.add_resource(Create_Request,'/Create_Request')

#JOB_TITLE is STILL the error change it to occupation

if __name__=="__main__":
	app.run()