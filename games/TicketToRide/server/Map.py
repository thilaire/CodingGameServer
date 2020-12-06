"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire
Licence: GPL

File: Map.py
    Contains the class Map for the TicketToRide game
    -> defines a map


To create a new map,
a) add its name in the definition of TicketToRide.map (see TicketToRide.py linee 62)
b) create a folder (with the same name as the map) in games/TicketToRide/maps/
c) with the following files
  - cities.csv:     list of cities (number;cityName)
  - tracks.csv:     list of tracks (city1;city2;length;track1 color;track2 color)
  - map.txt:        raw text for the map

Copyright 2020 T. Hilaire
"""

from itertools import zip_longest
from os.path import join
from csv import reader
from copy import copy
from importlib import import_module
from colorama import Fore, Back
from .Constants import colorNames
from .Track import Track
from .Objective import Objective


def decomment(csvfile):
	"""removes the comments in a csv file
	(comments start with #)
	do not take into account if the comment is in a string or not (not necessary here)
	"""
	for row in csvfile:
		raw = row.split('#')[0].strip()
		if raw:
			yield raw


class Map:
	"""One object Map per existing map is created
	The objects are created from the following files in the folder maps:
	- cities.csv    # list of the cities (with coordinates)
	- tracks.csv    # list of the tracks"""

	def __init__(self, name):
		"""create the object from the files"""
		# build the list of cities
		self._name = name

		self._coordinates = {}
		# import image coordinates, stored in python dict rather than json, no one likes parsing
		try:
			coo = import_module('games.TicketToRide.maps.' + name + '.coordinates')
			self._coordinates = coo.COORDINATES
		except:
			print("No coordinates data for Map "+name)

		with open(join('games', 'TicketToRide', 'maps', name, 'cities.csv')) as csvCities:
			cities = list(x for x in reader(decomment(csvCities), delimiter=';'))
		self._cities = [c[1] for c in cities]
		self._invCities = {c: i for i, c in enumerate(self._cities)}
		data = [c.replace(' ', '_') for c in self._cities]

		# open the text map and store it in a 2D array (list of lists)
		with open(join('games', 'TicketToRide', 'maps', name, 'map.txt')) as txtMap:
			self._rawtxt = [list(line[:-1]) for line in txtMap]

		# highlight the cities
		for c in cities:
			lin, col, size = [int(t) for t in c[2:5]]
			for dc in range(size):
				self._rawtxt[lin-1][col + dc-1] = Back.LIGHTWHITE_EX + Fore.BLACK + self._rawtxt[lin-1][col + dc-1] \
												  + Fore.RESET + Back.RESET


		# build the list of tracks
		with open(join('games', 'TicketToRide', 'maps', name, 'tracks.csv')) as csvTracks:
			self._tracks = []
			for i, track in enumerate(reader(decomment(csvTracks), delimiter=';')):
				try:
					# get the data
					cities = (self._invCities[track[0]], self._invCities[track[1]])
					length = int(track[2])
					col = (colorNames.index(track[3]), colorNames.index(track[4]))
					pos = (int(track[5]), int(track[6]))
					path = track[7]
					# build the track, and plot it (in rawtxt)
					tr = Track(cities, length, col, pos, path)
					self._tracks.append(tr)
					tr.draw(self._rawtxt)
				except KeyError:
					raise ValueError("The %dth element in %s contains an incorrect item: %s" % (
						i, join('maps', name, 'tracks.csv'), ';'.join(track)))
		data.extend(str(tr) for tr in self._tracks)

		# build the list of objectives
		with open(join('games', 'TicketToRide', 'maps', name, 'objectives.csv')) as csvObjectives:
			self._objectives = []
			for i, track in enumerate(reader(decomment(csvObjectives), delimiter=';')):
				try:
					# get the data
					city1 = self._invCities[track[0]]
					city2 = self._invCities[track[1]]
					score = int(track[2])
					self._objectives.append(Objective(city1, city2, score))
				except KeyError:
					raise ValueError("The %dth element in %s contains an incorrect item: %s" % (
						i, join('maps', name, 'objectives.csv'), ';'.join(track)))
		# build (once) the string to send to each client
		self._data = "\n".join(data)

	@property
	def name(self):
		return self._name

	@property
	def data(self):
		"""Returns the list of cities (with the space replaced by an underscore)
		and the tracks (5 integers by tracks)
		used to transmit the cities to the client"""
		return self._data


	@property
	def nbCities(self):
		"""Returns the number of cities"""
		return len(self._cities)

	def getCityName(self, city):
		"""Return the name of a city"""
		return self._cities[city]

	@property
	def nbTracks(self):
		"""Returns the number of tracks"""
		return len(self._tracks)

	@property
	def objectives(self):
		"""Return a list of copied objectives"""
		return [copy(o) for o in self._objectives]

	@property
	def rawtxt(self):
		"""Return the raw text"""
		# copy the list of list
		return [list(t) for t in self._rawtxt]

	@property
	def tracks(self):
		"""Return the tracks, a dictionary of the copy of the tracks"""
		# build the dictionary of tracks
		return {t.cities: copy(t) for t in self._tracks}

	@property
	def imagePath(self):
		return join('games', 'TicketToRide', 'maps', self._name, 'map.jpg')

	@property
	def imageCoordinates(self):
		return self._coordinates