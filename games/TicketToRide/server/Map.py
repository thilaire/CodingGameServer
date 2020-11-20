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

Copyright 2020 T. Hilaire
"""

from os.path import join
from csv import reader
from collections import namedtuple
from .Constants import colors
from CGSserver.Game import Game


class Track:
	def __init__(self, cities, length, col):
		self._cities = tuple(cities)
		self._length = length
		self._colors = tuple(col)

	def __str__(self):
		return "%d %d %d %d %d" % (self._cities[0], self._cities[1], self._length, self._colors[0], self._colors[1])


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
		with open(join('games', 'TicketToRide', 'maps', name, 'cities.csv')) as csvCities:
			self._cities = list(x[0] for x in reader(decomment(csvCities), delimiter=';'))
		self._invCities = {c: i for i, c in enumerate(self._cities)}
		data = [c.replace(' ', '_') for c in self._cities]

		# build the list of tracks
		with open(join('games', 'TicketToRide', 'maps', name, 'tracks.csv')) as csvTracks:
			self._tracks = []
			for i, track in enumerate(reader(decomment(csvTracks), delimiter=';')):
				try:
					# get the cities
					cities = (self._invCities[track[0]], self._invCities[track[1]])
					length = int(track[2])
					col = (colors[track[3]], colors[track[4]])
					self._tracks.append(Track(cities, length, col))
				except KeyError:
					raise ValueError("The %dth element in %s contains an incorrect item: %s" % (
										i, join('maps', name, 'tracks.csv'), ';'.join(track)))
		data.extend(str(tr) for tr in self._tracks)

		# build (once) the string to send to each client
		self._data = "\n".join(data)


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


	@property
	def nbTracks(self):
		"""Returns the number of tracks"""
		return len(self._tracks)
