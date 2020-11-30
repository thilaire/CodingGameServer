"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire
Licence: GPL

File: Map.py
	Contains the class Track for the TicketToRide game
	-> defines a track


Copyright 2020 T. Hilaire
"""

from .Constants import NONE, MULTICOLOR

class Track:
	"""simple class to store a track"""
	def __init__(self, cities, length, col):
		"""a track contains the two cities, the length and the colors"""
		self._cities = (min(cities), max(cities))
		self._length = length
		self._colors = tuple(col)
		self._taken = False      # True if taken by a player
		self._player = 0        # if taken, it gives the number of the player who have it

	def __str__(self):
		return "%d %d %d %d %d" % (self._cities[0], self._cities[1], self._length, self._colors[0], self._colors[1])

	@property
	def cities(self):
		"""return the cities"""
		return self._cities

	@property
	def isTaken(self):
		"""returns if the track is already taken"""
		return self._taken

	@property
	def length(self):
		"""Returns the length of the track"""
		return self._length

	def checkCards(self, card, nbCards, nbLocomotives):
		"""check if nbCards of color card, plus nbLocomotives locomotives can be used to claim the track
		Return True if the player can take the card, False otherwise
		HERE is the rule to claim a track (to be modified for Europe map, for example)
		"""
		# if the tracks is MULTICOLOR (ie with any determine color), then the player just needs enough card of its color
		# if the track is not MULTICOLOR, the player need to propose a color that is in the set of possible colors
		# and also he needs just enough card of the color
		if self._colors[0] != MULTICOLOR and card not in self._colors:
			return False
		return (nbLocomotives + nbCards) >= self._length

	def claims(self, player):
		"""Claim the track as taken by the player"""
		self._taken = True
		self._player = player

	@property
	def iterColors(self):
		"""return the color(s)
		generator that returns 1 or 2 colors"""
		yield self._colors[0]
		if self._colors[1] != NONE:
			yield self._colors[1]

