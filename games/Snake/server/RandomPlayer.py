"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire, T. Gautier
Licence: GPL

File: RandomPlayer.py
	Contains the class RandomPlayer
	-> defines a stupid player

Copyright 2019 T. Hilaire, T. Gautier
"""

from server.Player import TrainingPlayer
from .Constants import EAST, NORTH, SOUTH, WEST

class RandomPlayer(TrainingPlayer):
	"""
	class RandomPlayer

	Inherits from TrainingPlayer
	"""

	def __init__(self, **options):
		"""
		Initialize the Training Player

		You may use the options dictionary
		"""
		super().__init__('RandomPlayer')
		#
		# insert your code here to get/validate/store the options...
		#


	def playMove(self):
		"""
		Returns the move to play (string)
		"""
		#
		# insert your code here to find which move you want to do...
		#
		return "%d" % SOUTH

