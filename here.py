import requests
import json
from math import radians, sin, cos, acos, atan2, sqrt, degrees
from operator import methodcaller

#API Key = GMeB-1KoNJ0XvhlOn9VFe4GPRCIWMusT-B-dwIYVSb0oG22RXFiUoBxz3gNvq4dTX2LenL6HWQwXoyLs9oJyFOIPWGFLRkPpKXo1KfCnENimVObU_vKl1clzLYZNWnYx
#client ID = OkyFz7f00cpLklJ7lzfEHg

class Place:
	def __init__(self, name, lat, lon, rating):
		self.name = name
		self.latitude = lat
		self.longitude = lon
		self.rating = rating
		self.has_rating = False
	
	def get_name(self):
		return self.name;
	
	def get_latitude(self):
		return self.latitude
	
	def get_longitude(self):
		return self.longitude
	
	def get_rating(self):
		return self.rating

	def set_rating(self, rating):
		self.rating = rating
		self.has_rating = True

	def get_distance(self, destination):
		starting_latitude = radians(float(self.latitude))
		ending_latitude = radians(float(destination.get_latitude()))
		starting_longitude = radians(float(self.longitude))
		ending_longitude = radians(float(destination.get_longitude()))
		return 6371.01 * acos(sin(starting_latitude) * sin(ending_latitude) + cos(starting_latitude) * cos(ending_latitude) * cos(starting_longitude - ending_longitude))

	def get_has_rating(self):
		return self.has_rating

def query_header_constructor(query, at_bool, at_val, in_val):
	"""Generates a dictionary named headers which stores a common set of parameters for the get requests in search_query, autosuggest_query, and explore_query"""
	APP_ID = "JlpRxY5ZfJmmqFMIoiGe"
	APP_CODE = "_0Wcx47HZmzeB48BpMHGGg"
	headers = dict()
	headers["app_id"] = APP_ID
	headers["app_code"] = APP_CODE
	if query is not None:
		headers["q"] = query
	if at_bool:
		headers["at"] = at_val
	# else:
	# 	headers["in"] = in_val
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
	for x in range(0, min(number_of_places, len(results))):
		target_place = results[x]
		rating = None
		if "averageRating" in target_place:
			rating = target_place.get("averageRating")
		places.append(Place(target_place["title"], target_place["position"][0], target_place["position"][1], rating))
	return places

#fixing route
def search_query(query, number_of_places, at_bool, at_val, in_val, lat1, lon1, lat2, lon2):
	"""Does a search query(Nokia Here Places API) and returns a list of places"""
	url = query_url_constructor("/discover/search")
	headers = query_header_constructor(query, at_bool, at_val, in_val)
	headers["route"] = "[" + str(lat1) + "," + str(lon1) + "|" + str(lat2) + "," + str(lon2) + "];w=100000" 
	print(headers)
	r = requests.get(url, params=headers)
	s = json.loads(r.text)
	print(s)
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
	headers["cat"] = "eat-drink, sights-museums"
	print(headers)
	print("HEADERS ABOVE HERE")
	r = requests.get(url, params=headers)
	s = json.loads(r.text)
	print(s)
	results = s["results"]
	results = results["items"]
	# print(results)`
	# return places_lst_constructor(results, number_of_places)


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

place1 = Place("Seattle", 47.608013, -122.335167, None)
place2 = Place("San Francisco", 37.773972, -122.431297, None)
place3 = Place("Los Angeles", 34.052235, -118.243683, None)

#Test for four_category_lists
lst = search_query_route("Museum", 3, False, "47.608013,-122.335167", center_circle_constructor(place2, place1), 37.773972, -122.431297, 34.052235, -118.243683)
for x in range(0,3):
	print(lst[x].get_name())

# lst = search_query("Museum", 3, False, "47.608013,-122.335167", center_circle_constructor(place2, place1))
# for x in range(0,3):
# 	print(lst[x].get_name())


def four_category_lists(choices_list, number_of_places, at_bool, at_val, starting_place, destination):
	for category in choices_list:
		lst = search_query(category, number_of_places, at_bool, at_val, center_circle_constructor(starting_place, destination))
		for x in range(0, number_of_places):
			print(lst[x].get_name())


def yelp_api_call(term, latitude, longitude):
	#API Key = GMeB-1KoNJ0XvhlOn9VFe4GPRCIWMusT-B-dwIYVSb0oG22RXFiUoBxz3gNvq4dTX2LenL6HWQwXoyLs9oJyFOIPWGFLRkPpKXo1KfCnENimVObU_vKl1clzLYZNWnYx
	url = "https://api.yelp.com/v3/businesses/search"
	headers = {
        'Authorization': 'Bearer GMeB-1KoNJ0XvhlOn9VFe4GPRCIWMusT-B-dwIYVSb0oG22RXFiUoBxz3gNvq4dTX2LenL6HWQwXoyLs9oJyFOIPWGFLRkPpKXo1KfCnENimVObU_vKl1clzLYZNWnYx',
	}
	url_params = {
        'term': term.replace(' ', '+'),
        'latitude': latitude,
        'longitude': longitude,
        'limit': 10
    }
	response = requests.request('GET', url, headers=headers, params=url_params)
	s = json.loads(response.text)
	return s.get("businesses")

def yelp_api_set_rating(term, latitude, longitude):
	#uses yelp api to get a place's rating
	url = "https://api.yelp.com/v3/businesses/search"
	headers = {
        'Authorization': 'Bearer GMeB-1KoNJ0XvhlOn9VFe4GPRCIWMusT-B-dwIYVSb0oG22RXFiUoBxz3gNvq4dTX2LenL6HWQwXoyLs9oJyFOIPWGFLRkPpKXo1KfCnENimVObU_vKl1clzLYZNWnYx',
	}
	url_params = {
        'term': term.replace(' ', '+'),
        'latitude': latitude,
        'longitude': longitude,
        'limit': 10
    }
	response = requests.request('GET', url, headers=headers, params=url_params)
	s = json.loads(response.text)
	for place in s['businesses']:
		if place['name'] == term:
			rating = place['rating']
			return rating
	return "Place has no rating"

#ranks places to visit based on ratings
def place_ranker(lst_places):
	new_lst = sorted(lst_places, key=methodcaller('get_rating'))[::-1]
	to_return = []
	for place in new_lst:
		to_return.append(place.get_name())
	return to_return

#place ranker test cases
# place1 = Place("Seattle", 47.608013, -122.335167, 5.0)
# place2 = Place("San Francisco", 37.773972, -122.431297, 5.2)
# place3 = Place("Los Angeles", 34.052235, -118.243683, 5.0)
# place_ranker([place1, place2, place3])


#to set rating in place class(USE LATER)
# lst_places = list()
# for place in lst_places:
# 	rating = yelp_api_set_rating(place.get_name(), place.get_latitude, place.get_longitude)
# 	if type(rating) is not str:
# 		place.set_rating(rating)



#Test for four_category_lists

# choices = ['Museum', 'Restaurant', 'Retail', 'Leisure-outdoors']
# choice_places = []
# #for category in choices:
# lst = search_query('Museum', 20, False, "47.608013,-122.335167", center_circle_constructor(place2, place1))
# for x in range(0,3):
# 	lst1.append(lst[x].get_name())
# for place in choice_places:
# 	place.set_rating = yelp_api_call_rating(place.get_name, place.get_latitude, place.get_longitude)







# """1/4 Search Query + Finding Places + Routing API"""



# """ 
# # Test for autosuggest_query
# place_lst = autosuggest_query("chrysler", 3, True, "40.74917,-73.98529", None)
# first_place = place_lst[1]
# title = first_place.get_name()
# latitude = first_place.get_latitude()
# longitude = first_place.get_longitude()

# print(title)
# print(latitude)
# print(longitude) 
# """

# """
# # Test for search_query
# place_lst = search_query("chrysler", 3, True, "40.74917,-73.98529", None)
# first_place = place_lst[1]
# title = first_place.get_name()
# latitude = first_place.get_latitude()
# longitude = first_place.get_longitude()

# print(title)
# print(latitude)
# print(longitude)
# """
# """
# # Test for center_circle_constructor
# place1 = Place("Seattle", 47.608013, -122.335167, None)
# place2 = Place("San Francisco", 37.773972, -122.431297, None)
# print(center_circle_constructor(place1, place2))
# """
# place_lst = search_query("chrysler", 3, True, "40.74917,-73.98529", None)
# first_place = place_lst[1]
# title = first_place.get_name()
# latitude = first_place.get_latitude()
# longitude = first_place.get_longitude()

# print(title)
# print(latitude)
# place1 = Place("Seattle", 47.608013, -122.335167, None)
# place2 = Place("San Francisco", 37.773972, -122.431297, None)
# place3 = Place("Los Angeles", 34.052235, -118.243683, None)

# #Test for four_category_lists

# choices = ['Museum', 'Restaurant', 'Retail', 'Leisure-outdoors']


# for category in choices:
# 	lst = search_query(category, 20, False, "47.608013,-122.335167", center_circle_constructor(place2, place1))
# 	for x in range(0,20):
# 		print(lst[x].get_name())

# lst = search_query("Museum", 20, False, "47.608013,-122.335167", center_circle_constructor(place2, place1))
# for x in range(0,20):
# 	print(lst[x].get_name())


# lst = search_query("Museum", 20, False, "47.608013,-122.335167", center_circle_constructor(place3, place2))
# for x in range(0,20):
# 	print(lst[x].get_name())
#print(yelp_api_call("Intersection for the Arts", 37.76577, -122.42197))
#"https://api.yelp.com/v3/businesses/search"37.77828, -122.42926

