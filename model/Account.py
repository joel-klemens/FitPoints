#!/usr/bin/python3

"""
	File: Account.pys
    Name: Joel Klemens
    Date:  Feb 11, 2019
"""
from model import Activities
from model.Activities import Activity
from model.Activities import Run
from model.Activities import Gym
import json
from model.Database import Database

#*******************************************************************************************************
#class for account information
class Account_info():
	#total number of users
	user_count = 0

	def __init__(self, user_name, password, name_first, name_last, age, weight, height, num_activity):
		self.user_name = user_name
		self.password = password
		self.name_first = name_first
		self.name_last = name_last
		self.age = age
		self.height = height
		self.weight = weight
		self.num_activity = num_activity
		self.activity_list = []
		#add one to this counter everytime we add a new account
		Account_info.user_count += 1

	#***********************************************************************
	#Functions for account information 
	def get_point_total(self):
		total_points = 0
		for x in range(len(self.activity_list)):
			total_points += int(self.activity_list[x].points)
		return total_points

	def get_time_total(self):
		total_time = 0
		for x in range(len(self.activity_list)):
			total_time += int(self.activity_list[x].duration)
		return total_time

	def get_average_points(self):
		total_points = 0
		for x in range(len(self.activity_list)):
			total_points += int(self.activity_list[x].points)
		if (len(self.activity_list) > 0):
			return int(total_points/len(self.activity_list))
		return 0
	#***********************************************************************
	# accessors
	@property
	def user_name(self):
		return self.__user_name

	@property
	def password(self):
		return self.__password

	@property
	def name_first(self):
		return self.__name_first

	@property
	def name_last(self):
		return self.__name_last

	@property
	def age(self):
		return self.__age

	@property
	def height(self):
		return self.__height

	@property
	def weight(self):
		return self.__weight

	@property
	def num_activity(self):
		return self.__num_activity
	#***********************************************************************
	#mutators
	@user_name.setter
	def user_name(self, new_user_name):
		self.__user_name = new_user_name

	@password.setter
	def password(self, new_password):
		self.__password = new_password 

	@name_first.setter
	def name_first(self, new_name_first):
		self.__name_first = new_name_first

	@name_last.setter
	def name_last(self, new_name_last):
		self.__name_last = new_name_last

	@age.setter
	def age(self,new_age ):
		self.__age = new_age

	@height.setter
	def height(self, new_height):
		self.__height = new_height 

	@weight.setter
	def weight(self, new_weight):
		self.__weight = new_weight

	@num_activity.setter
	def num_activity(self, new_num_activity):
		self.__num_activity = new_num_activity

#*******************************************************************************************************
#list functions

#initializing the list of accounts
def init_account_list(account_list,database_obj): 
	#access the information on the stored user list from the database
	Database.init_account_list_db(database_obj, account_list)

#*******************************************************
def update_account_list(account_list, database_obj):
	#write the information in the account_list in the proper format to the main db_file
	#making an array to hold the information about the person 
	Database.update_db(database_obj, account_list)		

#*******************************************************
def check_user_pass(account_list, user_name, password): 
	#check if the user name and password are correct

	#adding a static login to bypass no longer 
	account_list.append(Account_info("J01", "1234", "Joel", "Klemens", "22", "70", "170", 3))

	for x in range(len(account_list)):
		if(user_name == account_list[x].user_name):
			if(password == account_list[x].password):
				return True
	return False

#*******************************************************
def search_user_name(account_list, user_name): 
	#search through the account list to make sure no two user names are the same
	for x in range(len(account_list)):
		if(user_name == account_list[x].user_name):
			return True
	return False 

#*******************************************************
def get_account_info(account_list, user_name):
	for x in range(len(account_list)):
		if(user_name == account_list[x].user_name):
			return account_list[x]

#*******************************************************
def open_user_logs(account_list, user_name):
	#get the account info object
	user = get_account_info(account_list, user_name) 

	if(int(user.num_activity) >= 0):
		#getting the account information from the database file
		with open("user_logs/"+user_name+".txt") as json_file:
		
			data = json.load(json_file)
			
			for p in data['user_data']:
				temp_type = p['activity_type']
				temp_HR = p['HR']
				temp_points = p['points'] 
				temp_duration = p['duration']
				temp_date = p['date']
				temp_notes = p['notes']
				if(temp_type == "run"):
					temp_distance = p['distance']
				if(temp_type == "gym"):
					temp_location = p['location']
				#add these to the activity list
				if(temp_type == "run"):
					user.activity_list.append(Run(temp_type, temp_HR, temp_points, temp_duration, temp_date, temp_notes, temp_distance))
				elif(temp_type == "gym"):
					user.activity_list.append(Gym(temp_type, temp_HR, temp_points, temp_duration, temp_date, temp_notes, temp_location))
				else:
					user.activity_list.append(Activity(temp_type, temp_HR, temp_points, temp_duration, temp_date, temp_notes))

			#close the file
			json_file.close() 

#*******************************************************
def update_user_logs(account_list, user_name):
	#hold the user data
	user_data = {}
	user_data['user_data'] = []

	#get the account info object
	user = get_account_info(account_list, user_name)

	for x in range(len(user.activity_list)):
		if(user.activity_list[x].activity_type == "run"):
			user_data['user_data'].append({
			'activity_type':user.activity_list[x].activity_type,
			'HR':user.activity_list[x].HR,
			'points':str(user.activity_list[x].points),
			'duration':user.activity_list[x].duration, 
			'date':user.activity_list[x].date, 
			'notes':user.activity_list[x].notes,
			'distance':user.activity_list[x].distance
			})
		elif(user.activity_list[x].activity_type == "gym"):
			user_data['user_data'].append({
			'activity_type':user.activity_list[x].activity_type,
			'HR':user.activity_list[x].HR,
			'points':str(user.activity_list[x].points),
			'duration':user.activity_list[x].duration, 
			'date':user.activity_list[x].date, 
			'notes':user.activity_list[x].notes,
			'location':user.activity_list[x].location
			})
		else:
			user_data['user_data'].append({
			'activity_type':user.activity_list[x].activity_type,
			'HR':user.activity_list[x].HR,
			'points':str(user.activity_list[x].points),
			'duration':user.activity_list[x].duration, 
			'date':user.activity_list[x].date, 
			'notes':user.activity_list[x].notes
			})

	with open('user_logs/'+user_name+'.txt', 'w+') as outfile:
		json.dump(user_data, outfile)
		#close the file
		outfile.close()
	print("json data: ")
	print(json.dumps(user_data))
