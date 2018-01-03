import requests
import json
from math import radians, sin, cos, acos, atan2, sqrt, degrees

class Place:
	def __init__(self, name, lat, lon, rating):
		self.name = name
		self.latitude = lat
		self.longitude = lon
		self.rating = rating
	
	def get_name(self):
		return self.name;
	
	def get_latitude(self):
		return self.latitude
	
	def get_longitude(self):
		return self.longitude
	
	def get_rating(self):
		return self.rating

	def get_distance(self, destination):
		starting_latitude = radians(float(self.latitude))
		ending_latitude = radians(float(destination.get_latitude()))
		starting_longitude = radians(float(self.longitude))
		ending_longitude = radians(float(destination.get_longitude()))
		return 6371.01 * acos(sin(starting_latitude) * sin(ending_latitude) + cos(starting_latitude) * cos(ending_latitude) * cos(starting_longitude - ending_longitude))

def query_header_constructor(query, at_bool, at_val, in_val):
	"""Generates a dictionary named headers which stores a common set of parameters for the get requests in search_query, autosuggest_query, and explore_query"""
	APP_ID = "JlpRxY5ZfJmmqFMIoiGe"
	APP_CODE = "_0Wcx47HZmzeB48BpMHGGg"
	headers = dict()
	headers["app_id"] = APP_ID
	headers["app_code"] = APP_CODE
	headers["q"] = query
	if at_bool:
		headers["at"] = at_val
	else:
		headers["in"] = in_val
	return headers

def query_url_constructor(entrypoint):
	"""Takes in an entrypoint and returns a url for hitting the Nokia Here Places API"""
	host = "https://places.api.here.com"
	path = "/places/v1/"
	entrypoint = entrypoint
	url = host + path + entrypoint
	body = ""
	return url

def places_lst_constructor(results, number_of_places):
	"""Takes in the results of a previous query and returns a list of Places with a size equal to the number of places requested"""
	places = []
	for x in range(0, number_of_places):
		target_place = results[x]
		rating = None
		if target_place.has_key(rating):
			rating = target_place.get(rating)
		places.append(Place(target_place["title"], target_place["position"][0], target_place["position"][1], rating))
	return places

def search_query(query, number_of_places, at_bool, at_val, in_val):
	"""Does a search query(Nokia Here Places API) and returns a list of places"""
	url = query_url_constructor("/discover/search")
	headers = query_header_constructor(query, at_bool, at_val, in_val)
	r = requests.get(url, params=headers)
	s = json.loads(r.text)
	results = s["results"]
	results = results["items"]
	return places_lst_constructor(results, number_of_places)

def autosuggest_query(query, number_of_places, at_bool, at_val, in_val):
	"""Does an autosuggest query(Nokia Here Places API) and returns a list of places"""
	url = query_url_constructor("/autosuggest")
	headers = query_header_constructor(query, at_bool, at_val, in_val)
	r = requests.get(url, params=headers)
	s = json.loads(r.text)
	results = s["results"]
	return places_lst_constructor(results, number_of_places)

def explore_query(query, number_of_places, at_bool, at_val, in_val):
	"""Does an explore query(Nokia Here Places API) and returns a list of places"""
	#Not fully functional, currently not parsing all of results
	url = query_url_constructor("/discover/explore")
	headers = query_header_constructor(query, at_bool, at_val, in_val)
	r = requests.get(url, params=headers)
	s = json.loads(r.text)
	results = s["results"]
	results = results["items"]
	return places_lst_constructor(results, number_of_places)


# def geobox_constructor(starting_place, destination):
# 	""" Takes in a starting place and a destination and makes a box the height of the United States with the width being between the two points"""

def center_circle_constructor(starting_place, destination):
	"""Takes in two places and returns a string representing a circle centered on the midpoint of the two places with a diameter that spans the distance between the two places"""
	dLon = radians(float(destination.get_longitude() - starting_place.get_longitude()))
	starting_latitude = radians(float(starting_place.get_latitude()))
	ending_latitude = radians(float(destination.get_latitude()))
	starting_longitude = radians(float(starting_place.get_longitude()))
	Bx = cos(ending_latitude) * cos(dLon)
	By = cos(ending_latitude) * sin(dLon)
	mid_latitude = atan2(sin(starting_latitude) + sin(ending_latitude), sqrt((cos(starting_latitude) + Bx) * (cos(starting_latitude) + Bx) + By * By))
	mid_longitude = starting_longitude + atan2(By, cos(starting_latitude) + Bx)
	radius = starting_place.get_distance(destination) / 2

	result = "" + str(degrees(mid_latitude)) + "," + str(degrees(mid_longitude)) + ";" + "r=" + str(radius)
	return result 



""" 
# Test for autosuggest_query
place_lst = autosuggest_query("chrysler", 3, True, "40.74917,-73.98529", None)
first_place = place_lst[1]
title = first_place.get_name()
latitude = first_place.get_latitude()
longitude = first_place.get_longitude()

print(title)
print(latitude)
print(longitude) 
"""

"""
# Test for search_query
place_lst = search_query("chrysler", 3, True, "40.74917,-73.98529", None)
first_place = place_lst[1]
title = first_place.get_name()
latitude = first_place.get_latitude()
longitude = first_place.get_longitude()

print(title)
print(latitude)
print(longitude)
"""
"""
# Test for center_circle_constructor
place1 = Place("Seattle", 47.608013, -122.335167, None)
place2 = Place("San Francisco", 37.773972, -122.431297, None)
print(center_circle_constructor(place1, place2))
"""
# place_lst = search_query("chrysler", 3, True, "40.74917,-73.98529", None)
# first_place = place_lst[1]
# title = first_place.get_name()
# latitude = first_place.get_latitude()
# longitude = first_place.get_longitude()

# print(title)
# print(latitude)

place1 = Place("Seattle", 47.608013, -122.335167, None)
place2 = Place("San Francisco", 37.773972, -122.431297, None)
print(center_circle_constructor(place1, place2))