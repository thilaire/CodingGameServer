"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire
Licence: GPL

File: Map.py
	Contains the class Objective for the TicketToRide game
	-> defines a objective


Copyright 2020 T. Hilaire
"""


class Objective:
	"""Simple class to store an objective"""
	def __init__(self, city1, city2, score):
		"""an objective is composed of two cities and the score"""
		self._city1 = city1
		self._city2 = city2
		self._score = score

	def __str__(self):
		"""return a string usued for communication with client"""
		return "%d %d %d" % (self._city1, self._city2, self._score)

	@property
	def city1(self):
		return self._city1

	@property
	def city2(self):
		return self._city2
