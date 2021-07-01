#!/usr/bin/python3

"""
	File: dataBase.py
    Name: Joel Klemens
    Date:  Feb 11, 2019
"""
import sys
import mysql.connector
import pymysql
from mysql.connector import errorcode


#try establishing connection to the database
#	connectDatabase()
	#now that connection has been made we need to try to create the tables in the database
#	createDataBaseTables()

#*******************************************************************************************************
#establish a connection to the database
#Most of this code 
class Database():
	def connect_database(self):
		#*****************************************************************************
		#*****************************************************************************
		#In this section the marker will have to enter their own information as 
		# we are suppose to make this private 
		# Open database connection
		db_name = "jklemens" #example for Bob Dole
		u_name = "jklemens" #example for Bob Dole
		passwd = "" #example
		#*****************************************************************************
		#*****************************************************************************

		self.db_name = db_name
		self.u_name = u_name
		self.passwd = passwd

		#here we are going to check for command line variables 
		numberOfArgs = len(sys.argv)
		loop_counter = 0
		attempt_flag = 0
		while(loop_counter != 3):
			try:
				conn = mysql.connector.connect(host="removed",database=self.db_name,user=self.u_name, password=self.passwd)
				print("Database message: Successfully connected to database.~")
				# prepare a cursor object using cursor() method
				cursor = conn.cursor()
				self.cursor = cursor
				self.conn = conn
			except mysql.connector.Error as err:
				print(END, "Error:{}\n".format(err))
				attempt_flag = 1
			if(attempt_flag == 1):
				attempt_flag = 0
				loop_counter = loop_counter + 1
				if(loop_counter == 3):
					messagebox.showinfo("Error","Could not connect to database")
					exit()
			else:
				loop_counter = 3

	#*******************************************************************************************************
	def create_database_table(self):
		#here we are going to try to create the DB tables required
		#try to make the table that will hold the information about the user
		create_user_table="create table USER_INFO (user_name varchar(100) not null, password varchar(100) not null, name_first varchar(100) not null, name_last varchar(100) not null, age varchar(100), height varchar(100), weight varchar(100), num_activity varchar(100), primary key(user_name))"
		try:
			self.cursor.execute(create_user_table)
			print("Database message: Table USER_INFO added to database")
		except mysql.connector.Error as err:
			#get the error, if the error is that the table already exists then we can continue
			if(err.errno == 1050):
				print("Database message: Table USER_INFO exists in database")
			else:
				print("Error:{}\n".format(err))

	#*******************************************************************************************************
	def db_name_pass(self):
			#ask the user to enter their database name and then their password
			self.db_name = simpledialog.askstring("Database address", "Please enter the address to the database you wish to open")
			self.passwd = simpledialog.askstring("Database password", "Please enter the password to access this database.")
	#*******************************************************************************************************
	def update_db(self, account_list):
		#here we will update the database with the users account information 
		for x in range(len(account_list)):
			new_record = "INSERT INTO USER_INFO (user_name,password,name_first,name_last,age,height,weight,num_activity) VALUES ('"+account_list[x].user_name+"','"+account_list[x].password+"','"+account_list[x].name_first+"','"+account_list[x].name_last+"','"+str(account_list[x].age)+"','"+str(account_list[x].height)+"','"+str(account_list[x].weight)+"','"+str(account_list[x].num_activity)+"')"
			try:
				self.cursor.execute(new_record)
				self.conn.commit()
				print("User added to database.\n")
			except mysql.connector.Error as err:
				if(err.errno == 1242):
					print("Error: user already in database\n")
				else:
					print("Error:{}\n".format(err))

	#*******************************************************************************************************
	def init_account_list_db(self, account_list):
		#imoprt account so that we can make the the object here
		from model.Account import Account_info
		#here we will get the information from the database to populate the account list
		num_user_Q = "SELECT COUNT(*) from USER_INFO"
		self.cursor.execute(num_user_Q)
		num_users = self.cursor.fetchone()[0]
		#check to see if the database is empty
		if(num_users == 0):
			print("Database empty - Please create account")
		else:
			#if it is not empty then we need to get the information from it 
			user_Q = "SELECT * from USER_INFO"
			self.cursor.execute(user_Q)
			for row in self.cursor:
				temp_user_name = row[0]
				temp_password = row[1]
				temp_name_first = row[2]
				temp_name_last = row[3]
				temp_age = row[4]
				temp_weight = row[5]
				temp_height = row[6]
				temp_num_activity = row[7]
				#create new object and add it to the account_list
				account_list.append(Account_info(temp_user_name, temp_password, temp_name_first, temp_name_last, temp_age, temp_weight, temp_height, int(temp_num_activity)))
						
