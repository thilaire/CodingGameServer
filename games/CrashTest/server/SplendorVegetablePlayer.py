"""
* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: B. Lamon, based on T. Hilaire & J. Brajard's template file.
Licence: GPL

File: SplendorVegetablePlayer.py
	Contains the class SplendorVegetablePlayer
	->	Vegetable Player.
		A bot that plays randomly following the rules (= random legal moves).

Copyright 2025 B. Lamon
"""
from random import randint
from CGSserver.Player import TrainingPlayer


class SplendorVegetablePlayer(TrainingPlayer):
	"""
	Vegetable Player.
	A bot that plays like a vegetable, a potato for instance.
	Although it is not enough to run a Genetic Lifeform and Disk Operating System (GLaDOS).
	And not enough to make good decisions, just like [insert sensitive decision, bonus point if it's a political one].
	And definitely not enough to run a LLM.

	Basically, a bot that plays random available moves.
	It shan't play illegal moves, otherwise it (= me because I programmed it) will be dumber than what I expected.
	"""

	def __init__(self, **options):
		"""
		Initialize the Training Player

		You may use the options dictionary
		"""
		# Randomly choose a name from a list of vegetables
		vegList = ["Carrot", "Broccoli", "Spinach", "Cabbage", "Zucchini", "Eggplant", "Cucumber", "Lettuce", "Radish", "Potato"]
		vegetableName = vegList[randint(0, len(vegList))]
		# init super class w/ vegetable name
		super().__init__(vegetableName)
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
		return ""

