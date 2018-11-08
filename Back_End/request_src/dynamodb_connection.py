import pdb
from flask import Flask, render_template
import pymysql
#store number 
#Add email
class Dynamodb_Connection:
	def __init__(self):
		'''
			set up private variables needed for connection/access to database
		'''
		self.__endpoint			= "shiftcoverdbinstance.cb6b8triq82g.us-east-1.rds.amazonaws.com"#render_template('endpoint')
		self.__username			= "ktravers"#render_template('username')
		self.__password			= "shift_cover"#render_template('password')
		self.__database			= "shiftcoverDB"#render_template('database')
		self.__conn 			= None
		self.__cursor			= None
		self.__table_hash 		= {"accounts":"accounts",
									"relationship":"relationship",
									"posts":"posts",
									"messages":"messages"}
		dynamodb = boto3.resource('dynamodb',region_name='us-east-1') 

	def __start_connection(self):
		'''
			Creates connection to database creating __conn(connection)
			and __cursor to execute sql commands
			Return Boolean false if something went wrong and connection failed
                        Inputs: None
                        Outputs: Boolean of Connection Status
		'''
		result = True
		try:
			self.__conn     = pymysql.connect(self.__endpoint,user=self.__username, password=self.__password,db=self.__database,connect_timeout=60)
			self.__cursor   = self.__conn.cursor()	
		except Exception as e:
			result = False
		finally:
			return result
	def __end_connection(self):
		'''
			closes connection to database, returns false if Connection failed to close
			Inputs: None
                        Outputs: Boolean of Connection Status
		'''
		result = True
		try:
			self.__conn.close()
		except Exception as e:
			self.__conn.rollback()
			result = False
		finally:
			return result
	def __execute(self,sql_command,sql_values):
		'''
			opens connection to database
			runs and commits command on to database
			return error message if failed
			closes connectin no matter what
			Input: String sql_command Dictionary sql_values
			Output: mysql output after command or error message if something went wrong 
		'''
		try:
			self.__start_connection()
			affect_rows = self.__cursor.execute(sql_command,sql_values)
			result 		= self.__cursor.fetchall()
			if not result:
				result = affect_rows
			#inserted new row
			#if self.__conn.insert_id():
				#print(self.__conn.insert_id())#None no insert number if inserted 
				#pass table along in future
				#account_id = self.__conn.insert_id()
				#sql_command="SELECT * FROM accounts WHERE  account_id = %(account_id)s;"
				#sql_values={"account_id":account_id}
				#result 		= self.__execute(sql_command,sql_values)
				
			#convert tupple rturned from mysql and instead return json
			if self.__cursor.description:
				row_headers =[row_header[0] for row_header in self.__cursor.description]
				json_data 	= []
				for data in result:
					json_data.append(dict(zip(row_headers,data)))
				if result:
					result = json_data
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			result = False
		finally:
			self.__end_connection()
			return result
	
	def get_row_by_id(self,data_hash):
		'''
			Returns account array [int(account_id),str(username),str(password),
                        str(account_picture) S3 bucket url to users account pic,
                        date Time user created account ]
                        All usernames are unique
			Inputs:  String username
			Outputs: account array 
		'''
		try:
			table_name 	= self.__table_hash["accounts"]
			sql_command     = "SELECT * FROM {}  WHERE username = %(username)s;".format(table_name)
			sql_values 	= {'username':username}
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result = False
		finally:
			return result
	def get_rows(self,data_hash):
		'''
			Return all accounts as array of arrays [[int(account_id),str(username),
			str(password), str(account_picture) S3 bucket url to users account pic,
                        date Time user created account]... ]
			Inputs: None
			Ouputs: Array of all accounts arrays
		'''
		try:
			table_name 	= self.__table_hash["accounts"]
			sql_command     = "SELECT * FROM {};".format(table_name)
			sql_values 	= {}
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result = False
		finally:
			return result
	def get_row(self,data_hash):
		'''
                        Check if username and hashed password exist in database
			Inputs:  String Username String Password
			Outputs: return account array if credientals are correct,
			Empty array if Credenitals are wrong
		'''
		try:
			table_name 	= self.__table_hash["accounts"]
			sql_command     = """SELECT * FROM {} WHERE username = %(username)s
                                        AND password = %(password)s;""".format(table_name)
			sql_values 	= {'username':username,
                                           "password":password}
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result = False
		finally:
			return result
	def update_row(self,data_hash):
		'''
            Update account for all fields in account, except account id
			Inputs: str(username),str(password),str(account_picture),Int(account_id)
			Outputs: return account array if credientals are correct,
			Empty array if Credenitals are wrong
		'''
		try:
			table_name 	= self.__table_hash["accounts"]
			sql_command     = """UPDATE {} SET username = %(username)s,
								password = %(password)s, account_picture = %(account_picture)s, job_title = %(occupation)s, 
								company = %(company)s, email = %(email)s, first_name = %(first_name)s, last_name = %(last_name)s
								WHERE account_id = %(account_id)s;""".format(table_name)
			sql_values 	= {'username':username,
							"password":password,
							"account_picture":account_picture,
							"occupation":occupation,
							"company":company,
							"email":email,
							"first_name":first_name,
							"last_name":last_name,
							"account_id":account_id}
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result = False
		finally:
			return result
	def delete_row(self, data_hash):
		'''
			Delete account from accounts database
			Inputs: Int account_id
			Outputs: None
		'''
		try:
			table_name 	= self.__table_hash["accounts"]
			sql_command = "DELETE FROM {} WHERE account_id = %(account_id)s;".format(table_name)
			sql_values 	= {'account_id':account_id}
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result 		= False	
			#raise e
		finally:
			return result
	
	def create_row(self,data_hash):
		#use connection.insert_id() to return the id of last inserted on this connection
		try:
			table_name 	= self.__table_hash["request"]
			sql_command     = """INSERT INTO {} (account_id,start_time,end_time,description,date_str) VALUES
			(%(account_id)s, %(start_time)s,%(end_time)s,%(description)s,%(date_str)s);""".format(table_name)
			sql_values 	= data_hash
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result 		= False	
			#raise e
		finally:
			return result		



