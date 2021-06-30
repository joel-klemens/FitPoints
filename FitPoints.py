#!/usr/bin/python3

"""
	File: FitPoints.py
    Name: Joel Klemens
    Date:  Feb 11, 2019
"""
import json

import requests
from suds.client import Client

from model import Account 
from model.Account import Account_info
from model.Account import init_account_list
from model.Account import update_account_list
from model.Account import check_user_pass
from model.Account import search_user_name
from model.Account import get_account_info
from model.Account import open_user_logs
from model.Account import update_user_logs

from model import Activities
from model.Activities import Activity
from model.Activities import Run
from model.Activities import Gym

from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import * 
from tkinter import simpledialog
from tkinter import ttk
from re import * 

from model.Database import Database

#*******************************************************************************************************
#empty list - will be global so that we can access in
account_list = []
#*******************************************************************************************************
class main_window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self,master)
		self.master.title("Fit Points")
		self.master.iconname("Fit Points")

		#main page frame
		self.main_frame_page = Frame(self.master)
		#main page buttons
		self.log_in_button = Button(self.main_frame_page, text = "Log In", width = 15, command=self.loggingIn)
		self.create_button = Button(self.main_frame_page, text = "Create Account", width = 15, command=self.createAcct)
		#main page label
		self.intro_label = Label(self.main_frame_page, text = "Welcome to Fit Points\nPlease enter your login or create an account")
		#put it on the screen
		self.intro_label.pack(side = TOP)
		self.log_in_button.pack(side = TOP)
		self.create_button.pack(side = TOP)
		self.main_frame_page.place(x = 300, y = 280)

		#open the main db file 
			#self.database_obj = Database()
			#Database.connect_database(self.database_obj)
		#make sure that the database has the required table
			#Database.create_database_table(self.database_obj)

		#init the account list with the account information 
			#init_account_list(account_list, self.database_obj)

		#call the example web api consumption
		self.rest()
		self.soap()

#*******************************************************************************************************
	#http://quotesondesign.com/wp-json/posts? - from link provided by Judi - Inspirational quotes
	def rest(self):
		req = requests.get('http://quotesondesign.com/wp-json/posts?')
		print("**********************")
		req = req.json()
		print(req)
		print("**********************")

	#https://jansipke.nl/examples-of-public-soap-web-services/ - Country information 
	def soap(self):
		url="http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"
		client = Client(url)
		
		result = client.service.CountryISOCode("Canada")
		print(result)
		result = client.service.CapitalCity("CA")
		print(result)
		result = client.service.CountryCurrency("CA")
		print(result)
		print("**********************")

#*******************************************************************************************************
	def update_home_page(self, user):
		#create the home page for the software
		self.user_current = user 
		#init the frames that will be used
		self.home_page_frame = Frame(self.master, bg = "#AF9F9C")
		self.name_area_frame = Frame(self.home_page_frame, bg = "grey", height = 200)
		self.total_area_frame = Frame(self.home_page_frame, bg = "grey", height = 200)
		self.previous_area_frame = Frame(self.home_page_frame, bg = "grey", height = 400)
		#spacer frames just for visual appeal
		self.space_frame_1 = Frame(self.home_page_frame, bg = "black")
		self.space_frame_2 = Frame(self.home_page_frame, bg = "black")
		self.space_frame_3 = Frame(self.home_page_frame, bg = "black")
		#frame to hold the activity buttons
		self.add_activity_button_frame = Frame(self.home_page_frame, bg = "grey")
		#add activity buttons
		self.add_activity_button_run = Button(self.add_activity_button_frame, text = "Add new run", command=self.add_new_activity_run)
		self.add_activity_button_gym = Button(self.add_activity_button_frame, text = "Add new gym workout", command=self.add_new_activity_gym)
		self.add_activity_button_other = Button(self.add_activity_button_frame, text = "Add new activity", command=self.add_new_activity_other)

		#************************************************
		#name Area stuff
		self.display_name = Label(self.name_area_frame, text = user.name_first + " " + user.name_last)
		self.display_point_total = Label(self.name_area_frame, text = "Total Points: " + str(user.get_point_total()))

		#************************************************
		#total area stuff
		self.total_time_label = Label(self.total_area_frame, text = "Total Time: " + str(user.get_time_total()))
		self.average_points_per_activity_label = Label(self.total_area_frame, text = " Average Points Per Activity: " + str(user.get_average_points()))

		#************************************************
		#previous activity area stuff
		self.previous_activities_label = Label(self.previous_area_frame, text = "Previous Activities:")

		#************************************************
		#update the previous activites 
		self.create_table()
		self.update_table(user)

		#************************************************
		#add everything to the screen
		self.home_page_frame.pack(expand = YES, fill = BOTH)
		#displaying the name - This is row 1
		self.display_name.pack(side = LEFT)
		self.display_point_total.pack(side = RIGHT)
		self.name_area_frame.pack(fill = BOTH)
		self.space_frame_1.pack(fill = BOTH)

		#row 2
		self.total_time_label.pack(side = LEFT)
		self.average_points_per_activity_label.pack(side = RIGHT)
		self.total_area_frame.pack(fill = BOTH)
		self.space_frame_2.pack(fill = BOTH)

		#row 3
		self.previous_activities_label.pack(side = LEFT)
		self.previous_area_frame.pack(fill = BOTH)
		self.space_frame_3.pack(fill = BOTH)

		#table
		self.treeview.pack(expand=True, fill='both')

		#row 4 - Activity buttons
		self.add_activity_button_other.pack(side = RIGHT)
		self.add_activity_button_gym.pack(side = RIGHT)
		self.add_activity_button_run.pack(side = RIGHT)
		self.add_activity_button_frame.pack(side = BOTTOM, fill = BOTH)

#*******************************************************************************************************
#functions that deal with the tree view table
	def calculate_points(self, HR, time):
		int_HR = int(HR)
		time_1 = int(time)
		if(169 < int_HR < 300):
			return (time_1*5)
		elif (149 < int_HR < 170):
			return (time_1*4)
		elif(129 < int_HR < 150):
			return (time_1*3)
		elif(114 < int_HR < 130):
			return (time_1*2)
		elif(int_HR < 115):
			return (time_1)
#*******************************************************************************************************
	#used because cant call functions with variables from buttons 
	def add_new_activity_run(self):
		self.add_new_activity(self.user_current, "run")

	def add_new_activity_gym(self):
		self.add_new_activity(self.user_current, "gym")

	def add_new_activity_other(self):
		self.add_new_activity(self.user_current, "other")

	def add_new_activity(self, user, type_activity):
		#when the add new button is pressed
		temp_duration = simpledialog.askstring("Duration", "Please enter the duration of the activity (minutes)")
		temp_date = simpledialog.askstring("Date", "Please enter the date as DD/MM/YYYY")
		temp_HR = simpledialog.askstring("Heart Rate", "Please enter your average heart rate for the activity")
		if (type_activity == "run"):
			temp_distance = simpledialog.askstring("Distance", "Please enter the distance of your run (KM)")
		if (type_activity == "gym"):
			temp_location = simpledialog.askstring("Location", "Please enter which gym you went to")
		temp_notes = simpledialog.askstring("Notes", "Please enter any notes about the activity")

		#have user confirm
		if (type_activity == "run"):
			tempString = "Type of Activity: Run\nDuration: " + temp_duration + "\nDate: " + temp_date + "\nHeart Rate: " + temp_HR + "\nDistance: " + temp_distance + "\nNotes: " + temp_notes
			answer = messagebox.askyesnocancel("Is this information correct?", str(tempString))
		elif (type_activity == "gym"):
			tempString = "Type of Activity: Gym\nDuration: " + temp_duration + "\nDate: " + temp_date + "\nHeart Rate: " + temp_HR + "\nLocation: " + temp_location + "\nNotes: " + temp_notes
			answer = messagebox.askyesnocancel("Is this information correct?", str(tempString))
		else:
			tempString = "Type of Activity: Other\nDuration: " + temp_duration + "\nDate: " + temp_date + "\nHeart Rate: " + temp_HR + "\nNotes: " + temp_notes
			answer = messagebox.askyesnocancel("Is this information correct?", str(tempString))

		if (answer == True):

			#check for errors
			error_check = True

			#check duration, date, HR, distance, location, notes
			if(temp_duration.isdigit() != True):
				error_check = False

			if ("~" in temp_date):
				error_check = False

			if(temp_HR.isdigit() != True):
				error_check = False

			if (type_activity == "run"):
				if(temp_distance.isdigit() != True):
					error_check = False

			if (type_activity == "gym"):
				if ("~" in temp_location):
					error_check = False

			if ("~" in temp_notes):
				error_check = False

			if(error_check == True):
				points = self.calculate_points(temp_HR, temp_duration)
				#add this to the users activities
				if(type_activity == "run"):
					user.activity_list.append(Run(type_activity, temp_HR, points, temp_duration, temp_date, temp_notes, temp_distance))
					user.num_activity += 1; 
					update_user_logs(account_list, user.user_name)
					self.update_table(user)
					messagebox.showinfo("Activity added", "Activity successfully added")

				elif(type_activity == "gym"):
					user.activity_list.append(Gym(type_activity, temp_HR, points, temp_duration, temp_date, temp_notes, temp_location))
					user.num_activity += 1; 
					update_user_logs(account_list, user.user_name)
					self.update_table(user)
					messagebox.showinfo("Activity added", "Activity successfully added")
				else:
					user.activity_list.append(Activity(type_activity, temp_HR, points, temp_duration, temp_date, temp_notes))
					user.num_activity += 1; 
					update_user_logs(account_list, user.user_name)
					self.update_table(user) 
					messagebox.showinfo("Activity added", "Activity successfully added")
			else:
				messagebox.showinfo("Activity not added", "There was an error with information added, please try again")

#*******************************************************************************************************
	#function to create the table that will have the workouts
	def create_table(self):
		comp_table = ttk.Treeview(self.home_page_frame)
		comp_table_sby = ttk.Scrollbar(orient="vertical", command=comp_table.yview)
		comp_table_sbx = ttk.Scrollbar(orient="horizontal", command=comp_table.xview)
		comp_table.configure(yscrollcommand=comp_table_sby.set,xscrollcommand=comp_table_sbx.set)
		comp_table['columns'] = ('Activity', 'Points', 'Date', 'Summary')
		comp_table.heading("#0", text='#', anchor='w')
		comp_table.column("#0", anchor="w", width=60)
		comp_table.heading('Activity', text='Activity')
		comp_table.column('Activity', anchor='center', width=60)
		comp_table.heading('Points', text='Points')
		comp_table.column('Points', anchor='center', width=60)
		comp_table.heading('Date', text='Date')
		comp_table.column('Date', anchor='center', width=60)
		comp_table.heading('Summary', text='Summary')
		comp_table.column('Summary', anchor='center', width=400)
		self.treeview = comp_table
		self.update_table(self.user_current)

	#function is used to update the table that is in the home page
	def update_table(self, user):
		#clear the table 
		for x in self.treeview.get_children():
			self.treeview.delete(x)
		#refresh it with new elements
		for x in range(len(user.activity_list)):
			self.treeview.insert('', 0, text = x+1, values = (user.activity_list[x].activity_type, user.activity_list[x].points, user.activity_list[x].date, user.activity_list[x].notes))

		#update the totals 
		self.display_point_total.pack_forget()
		self.total_time_label.pack_forget()
		self.average_points_per_activity_label.pack_forget()
		self.display_point_total = Label(self.name_area_frame, text = "Total Points: " + str(user.get_point_total()))
		self.total_time_label = Label(self.total_area_frame, text = "Total Time: " + str(user.get_time_total()))
		self.average_points_per_activity_label = Label(self.total_area_frame, text = " Average Points Per Activity: " + str(user.get_average_points()))
		self.display_point_total.pack(side = RIGHT)
		self.total_time_label.pack(side = LEFT)
		self.average_points_per_activity_label.pack(side = RIGHT)

#*******************************************************************************************************
	def createAcct(self):
		#remove the main menu buttons
		self.main_frame_page.place_forget()
		#create the buttons for this page
		self.create_account_frame = Frame(self.master)
		self.create_account_back_button = Button(self.create_account_frame, text = "Back", width = 10, command=self.back_to_main_create)
		self.create_account_button_2 = Button(self.create_account_frame, text = "Create Account", width = 10, command=self.create_new_account)
		#take in variables of user name, password, name, age, weight
		self.ca_label_1 = Label(self.create_account_frame, text = "User name may include numbers and letters", fg = "red")
		self.ca_label_2 = Label(self.create_account_frame, text = "Password may include numbers, letters and symbols", fg = "red")
		self.ca_label_3 = Label(self.create_account_frame, text = "Make sure not to include any spaces!", fg = "red")
		#user_name
		self.get_user_frame = Frame(self.create_account_frame)
		self.get_user_field = Entry(self.get_user_frame, bd = 5)
		self.get_user_field_label = Label(self.get_user_frame, text = "User Name: ")
		self.get_user_field.pack(side = RIGHT)
		self.get_user_field_label.pack(side = LEFT)

		#password
		self.get_pass_frame = Frame(self.create_account_frame)
		self.get_pass_field = Entry(self.get_pass_frame, show = "*", bd = 5)
		self.get_pass_field_label = Label(self.get_pass_frame, text = "Password:   ")
		self.get_pass_field.pack(side = RIGHT)
		self.get_pass_field_label.pack(side = LEFT)

		#name_first
		self.get_name_first_frame = Frame(self.create_account_frame)
		self.get_name_first_field = Entry(self.get_name_first_frame, bd = 5)
		self.get_name_first_label = Label(self.get_name_first_frame, text = "First:          ")
		self.get_name_first_field.pack(side = RIGHT)
		self.get_name_first_label.pack(side = LEFT)

		#name_last
		self.get_name_last_frame = Frame(self.create_account_frame)
		self.get_name_last_field = Entry(self.get_name_last_frame, bd = 5)
		self.get_name_last_label = Label(self.get_name_last_frame, text = "Last:           ")
		self.get_name_last_field.pack(side = RIGHT)
		self.get_name_last_label.pack(side = LEFT)

		#age
		self.get_age_frame = Frame(self.create_account_frame)
		self.get_age_field = Entry(self.get_age_frame, bd = 5)
		self.get_age_field_label = Label(self.get_age_frame, text = "Age:             ")
		self.get_age_field.pack(side = RIGHT)
		self.get_age_field_label.pack(side = LEFT)

		#height
		self.get_height_frame = Frame(self.create_account_frame)
		self.get_height_field = Entry(self.get_height_frame, bd = 5)
		self.get_height_field_label = Label(self.get_height_frame, text = "Height (cm):")
		self.get_height_field.pack(side = RIGHT)
		self.get_height_field_label.pack(side = LEFT)

		#weight
		self.get_weight_frame = Frame(self.create_account_frame)
		self.get_weight_field = Entry(self.get_weight_frame, bd = 5)
		self.get_weight_field_label = Label(self.get_weight_frame, text = "Weight (Kg):")
		self.get_weight_field.pack(side = RIGHT)
		self.get_weight_field_label.pack(side = LEFT)

		#add everything to the frame
		self.ca_label_3.pack(side = TOP)
		self.get_user_frame.pack(side = TOP)
		self.ca_label_1.pack(side = TOP)
		self.get_pass_frame.pack(side = TOP)
		self.ca_label_2.pack(side = TOP)
		self.get_name_first_frame.pack(side = TOP)
		self.get_name_last_frame.pack(side = TOP)
		self.get_age_frame.pack(side = TOP)
		self.get_height_frame.pack(side = TOP) 
		self.get_weight_frame.pack(side = TOP)
		self.create_account_back_button.pack(side = LEFT)
		self.create_account_button_2.pack(side = RIGHT)
		self.create_account_frame.place(x = 250, y = 280)

	def back_to_main_create(self):
		#remove everything from the create account screen
		self.create_account_frame.place_forget() 
		self.main_frame_page.place(x = 300, y = 280) 

	def create_new_account(self):
		#for error handling
		errors = []
		regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
		
		#to create an account we need to have an object for account then ask the user to enter variables
		#take the variables check them and then attempt to create a new account
		
		#*****************************
		temp_user_name = self.get_user_field.get()
		#error handling 
		if (" " in temp_user_name):
			errors.append("Spaces in User Name")
		elif (regex.search(temp_user_name) != None):
			errors.append("Symbols in User Name")
		elif search_user_name(account_list, temp_user_name) != False:
			errors.append("User already exists")
		elif("" == temp_user_name):
			errors.append("Empty User Name")
		#*****************************
		temp_password = self.get_pass_field.get()
		if (" " in temp_password):
			errors.append("Spaces in Password")
		elif("" == temp_password):
			errors.append("Empty Password")
		#*****************************
		temp_name_first = self.get_name_first_field.get()
		if (" " in temp_name_first):
			errors.append("Spaces in First Name")
		elif("" == temp_name_first):
			errors.append("Empty First Name")
		#*****************************
		temp_name_last = self.get_name_last_field.get()
		if (" " in temp_name_last):
			errors.append("Spaces in Last Name")
		elif("" == temp_name_last):
			errors.append("Empty Last Name")
		#*****************************
		temp_age = self.get_age_field.get()
		if (" " in temp_age):
			errors.append("Spaces in Age")
		elif (temp_age.isdigit() != True):
			errors.append("Age is invalid")
		elif("" == temp_age):
			errors.append("Empty Age")
		#*****************************
		temp_weight = self.get_weight_field.get()
		if (" " in temp_weight):
			errors.append("Spaces in Weight")
		elif (temp_weight.isdigit() != True):
			errors.append("Weight is invalid")
		elif("" == temp_weight):
			errors.append("Empty Weight")
		#*****************************
		temp_height = self.get_height_field.get()
		if (" " in temp_height):
			errors.append("Spaces in Height")
		elif (temp_height.isdigit() != True):
			errors.append("Height is invalid")
		elif("" == temp_height):
			errors.append("Empty Height")
		#*****************************

		#check if there were errors
		if len(errors) != 0:
			errorString = ', '.join(map(str, errors))
			messagebox.showinfo("Error", errorString)
		else:
			#pop up telling them what the errors were
			messagebox.showinfo("Account Created", "Successfully created account: " + temp_user_name)
			account_list.append(Account_info(temp_user_name, temp_password, temp_name_first, temp_name_last, temp_age, temp_weight, temp_height, 0))
			#create them a file in the database
			temp_file = open("user_logs/"+temp_user_name+".txt", "w+")
			update_account_list(account_list, self.database_obj) 
			self.create_account_frame.place_forget() 
			self.update_home_page(get_account_info(account_list, temp_user_name))


#*******************************************************************************************************
	def loggingIn(self):
		#remove the main menu buttons
		self.main_frame_page.place_forget()
		#create the buttons for the log in page
		self.log_in_page = Frame(self.master)
		self.log_in_back_button = Button(self.log_in_page, text = "Back", width = 10, command=self.backToMainLog)
		self.log_in_button_2 = Button(self.log_in_page, text = "Log In", width = 10, command=self.checkLogIn)

		#text feild for user name  
		self.user_frame = Frame(self.log_in_page)
		self.user_field = Entry(self.user_frame, bd = 5)
		self.user_field_label = Label(self.user_frame, text = "User Name: ")
		self.user_field.pack(side = RIGHT)
		self.user_field_label.pack(side = LEFT)

		#text feild for password
		self.pass_frame = Frame(self.log_in_page)
		self.pass_field = Entry(self.pass_frame, show = "*", bd = 5)
		self.pass_field_label = Label(self.pass_frame, text = "Password:   ")
		self.pass_field.pack(side = RIGHT)
		self.pass_field_label.pack(side = LEFT)

		#put everything into the log in page frame
		self.user_frame.pack(side = TOP)
		self.pass_frame.pack(side = TOP)
		self.log_in_back_button.pack(side = LEFT)
		self.log_in_button_2.pack(side = RIGHT)
		self.log_in_page.place(x = 250, y = 280)

	def backToMainLog(self):
		#remove everything from the log in screen 
		self.log_in_page.place_forget() 
		self.main_frame_page.place(x = 300, y = 280) 

	def checkLogIn(self):
		#check the database for the user_name and password
		temp_user_name = self.user_field.get()
		temp_password = self.pass_field.get() 

		if(check_user_pass(account_list, temp_user_name, temp_password) == True):
			messagebox.showinfo("Log in Status", "Successfully logged in")
			open_user_logs(account_list, temp_user_name)
			self.log_in_page.place_forget()
			self.update_home_page(get_account_info(account_list, temp_user_name)) 
		else:
			messagebox.showinfo("Log in Status", "Incorrect user_name or password")

#*******************************************************************************************************
#************************************************
root = Tk()

root.geometry("800x800")
root.configure(background='grey')
app = main_window(root)

root.mainloop() 
#************************************************