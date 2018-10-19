import pdb
from flask import Flask, render_template
import pymysql

class DB_Connection:
	def __init__(self):
		'''
			set up private variables needed for connection/access to database
		'''
		self.__endpoint			= "shiftcoverdbinstance.cb6b8triq82g.us-east-1.rds.amazonaws.com"#render_template('endpoint')
		self.__username			= "ktravers"#render_template('username')
		self.__password			= "shift_cover"#render_template('password')
		self.__profile_table	        = "profiles"#render_template('profiles')
		self.__database			= "shiftcoverDB"#render_template('database')
		self.__conn 			= None
		self.__cursor			= None
		self.__table_hash 		= {"profiles":self.__profile_table,
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
			result = "Their was error {}".format(e)
			raise e
		finally:
			self.__end_connection()
			return result
	#PROFILES
	def create_profile(self,username,password,profile_pic,role,company):
		'''
			create profile with username and password unless username is already taken
			Inputs: String username string password
				password will be hashed earlier
			Outputs: Success or error message
		
		'''
		try:
			table_name 	= self.__table_hash["profiles"]
			sql_command     = """INSERT INTO {} (username,password,profile_pic,role,company) VALUES
                                        (%(username)s, %(password)s,%(profile_pic)s,%(role)s,%(company)s);""".format(table_name)
			sql_values 	= {'username':username,
                                           "password":password,
                                           "profile_pic":profile_pic,
                                           "role":role,
                                           "company":company}
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result = "Their was error creating profile {}".format(e)	
			raise e
		finally:
			return result
	def get_profile(self,username):
		'''
			Returns profile array [int(profile_id),str(username),str(password),
                        str(profile_pic) S3 bucket url to users profile pic,
                        date Time user created account ]
                        All usernames are unique
			Inputs:  String username
			Outputs: profile array 
		'''
		try:
			table_name 	= self.__table_hash["profiles"]
			sql_command     = "SELECT * FROM {}  WHERE username = %(username)s;".format(table_name)
			sql_values 	= {'username':username}
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result = "Their was error getting profile {}".format(e)	
			raise e
		finally:
			return result
	def get_profiles(self):
		'''
			Return all profiles as array of arrays [[int(profile_id),str(username),
			str(password), str(profile_pic) S3 bucket url to users profile pic,
                        date Time user created account]... ]
			Inputs: None
			Ouputs: Array of all profiles arrays
		'''
		try:
			table_name 	= self.__table_hash["profiles"]
			sql_command     = "SELECT * FROM {};".format(table_name)
			sql_values 	= {}
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result = "Their was error getting profiles {}".format(e)	
			raise e
		finally:
			return result
	def profile_login(self,username,password):
		'''
                        Check if username and hashed password exist in database
			Inputs:  String Username String Password
			Outputs: return Profile array if credientals are correct,
			Empty array if Credenitals are wrong
		'''
		try:
			table_name 	= self.__table_hash["profiles"]
			sql_command     = """SELECT * FROM {} WHERE username = %(username)s
                                        AND password = %(password)s;""".format(table_name)
			sql_values 	= {'username':username,
                                           "password":password}
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result = "Their checking credientals {}".format(e)	
			raise e
		finally:
			return result
	def update_profile(self,username,password,profile_pic,role,company):
		'''
                        Update profile for all fields in profile, except profile id
			Inputs: str(username),str(password),str(profile_pic),Int(profile_id)
			Outputs: return Profile array if credientals are correct,
			Empty array if Credenitals are wrong
		'''
		try:
			table_name 	= self.__table_hash["profiles"]
			sql_command     = """UPDATE {} SET username = %(username)s,
                                        password = %(password)s, profile_pic = %(profile_pic)s, role = %(role)s, company = %(company)s
                                        WHERE profile_id = %(profile_id)s;""".format(table_name)
			sql_values 	= {'username':username,
                                           "password":password,
                                           "profile_pic":profile_pic,
                                           "role":role,
                                           "company":company}
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result = "Their was updating profile {}".format(e)	
			raise e
		finally:
			return result
	def delete_profile(self, profile_id):
		'''
			Delete profile from profiles database
			Inputs: Int profile_id
			Outputs: None
		'''
		try:
			table_name 	= self.__table_hash["profiles"]
			sql_command     = "DELETE FROM {} WHERE profile_id = %(profile_id)s;".format(table_name)
			sql_values 	= {'profile_id':profile_id}
			result 		= self.__execute(sql_command,sql_values)
		except Exception as e:
			result = "Their was error deleting profile {}".format(e)	
			raise e
		finally:
			return result
	





