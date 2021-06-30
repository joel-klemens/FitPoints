#!/usr/bin/python3

"""
	File: Activity.py
    Name: Joel Klemens
    Date:  Feb 11, 2019
"""

#*******************************************************************************************************
#class for types of activities
class Activity():
	def __init__(self, activity_type, HR, points, duration, date, notes):
		self.activity_type = activity_type
		self.HR = HR
		self.points = points
		self.duration = duration
		self.date = date
		self.notes = notes

	#***********************************************************************
	# accessors
	@property
	def activity_type(self):
		return self.__activity_type

	@property
	def HR(self):
		return self.__HR

	@property
	def points(self):
		return self.__points

	@property
	def duation(self):
		return self.__duration

	@property
	def date(self):
		return self.__date

	@property
	def notes(self):
		return self.__notes

	#Mutators
	@activity_type.setter
	def activity_type(self, new_activity_type):
		self.__activity_type = new_activity_type

	@HR.setter
	def HR(self, new_HR):
		self.__HR = new_HR

	@points.setter
	def points(self, new_points):
		self.__points = new_points

	@duation.setter
	def duation(self, new_duation):
		self.__duation = new_duation

	@date.setter
	def date(self, new_date):
		self.__date = new_date

	@notes.setter
	def notes(self, new_notes):
		self.__notes = new_notes

#extens activity
class Run(Activity):
	def __init__(self, activity_type, HR, points, duration, date, notes, distance):
		super().__init__(activity_type, HR, points, duration, date, notes)
		self.distance = distance

	@property
	def distance(self):
		return self.__distance

	@distance.setter
	def distance(self, new_distance):
		self.__distance = new_distance

#extends activity
class Gym(Activity):
	def __init__(self, activity_type, HR, points, duration, date, notes, location):
		super().__init__(activity_type, HR, points, duration, date, notes)
		self.location = location

	@property
	def location(self):
		return self.__location

	@location.setter
	def location(self, new_location):
		self.__location = new_location

