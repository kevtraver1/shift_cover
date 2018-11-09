import pdb
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

class Dynamodb_Connection:
	def __init__(self):
		self.__dynamodb 	= boto3.resource('dynamodb',region_name='us-east-1') 
		self.__table 		= self.__dynamodb.Table('shift_request')
		self.__scheme 		= {"date":None,"start_time":None}
	def get_item(self,data_hash):
		try:
			response = self.__table.get_item(
				Key=data_hash
			)
		except (ClientError, Exception)as e:
			return "error getting item {}".format(e.response['Error']['Message'])
		return response['Item']
	def insert_item(self,data_hash):
		try:
			result = self.__table.put_item(
				Item=data_hash
			)
		except (ClientError, Exception)as e:
			result = 0
			return e.response['Error']['Message']
		return result


	def delete_item(self,data_hash):
		try:
			response = self.__table.delete_item(
				Key=data_hash
			)
		except (ClientError, Exception)as e:
			return "error deleting item {}".format(e.response['Error']['Message'])
		return response
	def get_items(self,data_hash):
		pass
