import pdb
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

class Dynamodb_Connection:
	def __init__(self):
		try:
			self.data = "INITIATING CONNECTION"
		except Exception as e:
			raise "Error in init {}".format(e)

	def insert_row(self):
		try:
			step = 0
			dynamodb = boto3.resource('dynamodb',region_name='us-east-1') 
			step = 1

			table = dynamodb.Table('shift_request')
			step = 2
			response = table.get_item(
				Key={"request_id": "Kevin","date":"today"}
			)
			step = 3

		except (ClientError, Exception)as e:
			return e.response['Error']['Message']
		return response['Item']