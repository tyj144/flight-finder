import datetime
from dateutil import parser
from datetime import date, time, datetime, timedelta
from random import randint
import pickle
import os


# Gathering user inputs
#user_location = raw_input("Enter your starting location (ex. SFO, LAX, SEA) : ").upper()
#user_s_time = raw_input("Enter your starting time (ex. 1/12/1999): ")
#user_e_time = raw_input("Enter your ending time (ex. 1/20/1999): ")

with open(os.path.dirname(os.path.realpath(__file__)) + "/flights.pickle", "rb") as f:
	flights = pickle.load(f)

#Checking if flights are starting from the correct location
def correct_location(start):
	location_flights = []

	for flight in flights:	
		if start == flight[0]:
			location_flights.append(flight)
		else:
			pass
	return location_flights

#Checking if flights are starting at the correct time
def correct_time(s_time , location_flights):
	matching_flights = []
	for flight in location_flights:
		if s_time == flight[2]:
			matching_flights.append(flight)
		else:
			pass 
	return matching_flights

# print(matching_flights)

# Checking for return flights
able_return_flights = []
def return_flights(end_time , m_flights):
	if (len(m_flights) - 1) < 0 :
		#print('No available flights at this time and location')
		able_return_flights[:] = []
		return None
	else:
		
		index = randint(0 , len(m_flights)-1)
		flight = m_flights[index]
		possbile_return_flights = correct_time(end_time, correct_location(flight[1]))
		for p in possbile_return_flights:
			if p[1] == flight[0]:
				able_return_flights.append(p)
			else:
				pass
		if able_return_flights == []:
			m_flights.pop(index)
			return_flights(end_time, m_flights)
		else:
			return_fl = list(able_return_flights)
			able_return_flights[:] = []
			return (flight, return_fl)

#print((correct_time(user_e_time , (correct_location(user_location , flight_list)))))

# Function that checks if a return flight exists:
#	for flight in matching_flights:
#		if flight[1] == returnf in flight_time_change:



def flight_finder(user_location, user_s_time, user_e_time):
	return_tuple = return_flights(user_e_time, correct_time(user_s_time , correct_location(user_location)))
	if return_tuple == None:
		pass
	else:
		flight, able_return_flights = return_tuple
		if able_return_flights == []:
			print("shouldn't happen")
		else:
			index2 = randint(0, len(able_return_flights) - 1)
			flight_choice = (flight, able_return_flights[index2])
			return flight_choice

#print(flight_finder("BOS", datetime(2017, 12, 3, 0, 0, 0).date(), datetime(2017, 12, 10, 0, 0, 0).date()))