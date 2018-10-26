import pdb
from flask import Flask, render_template
import pymysql


#Add email
class DB_Connection:
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
									"ratings":"ratings",
									"comments":"comments",
									"messages":"messages"}
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
			self.__cursor.execute(sql_command,sql_values)
			result = self.__cursor.fetchall()
			self.__conn.commit()
		except Exception as e:
			return False
		finally:
			self.__end_connection()
			return result
	#accounts
	def create_account(self,username,password,company,role,account_pic):
		'''
			create account with username and password unless username is already taken
			Inputs: String username string password
				password will be hashed earlier
			Outputs: Success or error message
		
		'''
		try:
			table_name 	= self.__table_hash["accounts"]
			sql_command     = """INSERT INTO {} (username,password,account_pic,role,company) VALUES
                                        (%(username)s, %(password)s,%(account_pic)s,%(role)s,%(company)s);""".format(table_name)
			sql_values 	= {'username':username,
                                           "password":password,
                                           "account_pic":account_pic,
                                           "role":role,
                                           "company":company}
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result = False
		finally:
			return result
	def get_account(self,username):
		'''
			Returns account array [int(account_id),str(username),str(password),
                        str(account_pic) S3 bucket url to users account pic,
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
	def get_accounts(self):
		'''
			Return all accounts as array of arrays [[int(account_id),str(username),
			str(password), str(account_pic) S3 bucket url to users account pic,
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
	def account_login(self,username,password):
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
	def update_account(self,username,password,company,role,account_pic,account_id):
		'''
            Update account for all fields in account, except account id
			Inputs: str(username),str(password),str(account_pic),Int(account_id)
			Outputs: return account array if credientals are correct,
			Empty array if Credenitals are wrong
		'''
		try:
			table_name 	= self.__table_hash["accounts"]
			sql_command     = """UPDATE {} SET username = %(username)s,
                                        password = %(password)s, account_pic = %(account_pic)s, role = %(role)s, company = %(company)s
                                        WHERE account_id = %(account_id)s;""".format(table_name)
			sql_values 	= {'username':username,
                                           "password":password,
                                           "account_pic":account_pic,
                                           "role":role,
                                           "company":company,
                                           "account_id":account_id}
			result 		= self.__execute(sql_command,sql_values)
			result 		= True
		except Exception as e:
			result = False
		finally:
			return result
	def delete_account(self, account_id):
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
	





