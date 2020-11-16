"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire
Licence: GPL

File: TicketToRide.py
	Contains the class T2R
	-> defines the Ticket To Ride game (its rules, moves, etc.)

Copyright 2020 T. Hilaire
"""

from CGSserver.Constants import NORMAL_MOVE, WINNING_MOVE, LOSING_MOVE
from CGSserver.Game import Game

# import here your training players
from .TemplateTrainingPlayer import TemplateTrainingPlayer


class T2R(Game):
	"""
	class T2R (Ticket To Ride)

	Inherits from Game
	- _players: tuple of the two players
	- _logger: logger to use to log infos, debug, ...
	- _name: name of the game
	- _whoPlays: number of the player who should play now (0 or 1)
	- _waitingPlayer: Event used to wait for the players
	- _lastMove, _last_return_code: string and returning code corresponding to the last move

	Add some properties
	- ...
	"""

	# dictionary of the possible training Players (name-> class)
	type_dict = {"DO_NOTHING": DoNothingPlayer}



	def __init__(self, player1, player2, **options):
		"""
		Create a game
		:param player1: 1st Player
		:param player2: 2nd Player
		:param options: dictionary of options (the options 'seed' and 'timeout' are managed by the Game class)
		"""
		#
		# insert your code here to create your game (its data, etc.)...
		#

		# call the superclass constructor (only at the end, because the superclass constructor launches
		# the players and they will immediately requires some Labyrinth's properties)
		super().__init__(player1, player2, **options)



	def HTMLrepr(self):
		"""Returns an HTML representation of your game"""
		# this, or something you want...
		return "<A href='/game/%s'>%s</A>" % (self.name, self.name)

	def getDictInformations(self, firstTime=False):
		"""
		Returns a dictionary for HTML display
		- firstTime is True when this is called for the 1st time by a websocket
		:return:
		"""
		#
		# insert your code here...
		#

		return {}

	def __str__(self):
		"""
		Convert a Game into string (to be send to clients, and display)
		"""
		# create your display (with datas of your game, players' name, etc.)
		# the comments are managed by the Game class

		#
		# insert your code here...
		#

		return ""


	def updateGame(self, move):
		"""
		update the game by playing a move
		- move: a string
		Return a tuple (move_code, msg), where
		- move_code: (integer) 0 if the game continues after this move, >0 if it's a winning move, -1 otherwise (illegal move)
		- msg: a message to send to the player, explaining why the game is ending
		"""
		# parse the move and check if it's in correct form
		# returns the tuple (LOOSING_MOVE, "The move is not in correct form  !") if not valid

		# check if the move is possible
		# returns (LOOSING_MOVE, "explanations....") if not valid (give the full reason why it is not valid)

		# move the player
		# update the intern data
		# use self._whoPlays to get who plays (0 or 1)

		# if won, returns the tuple (WINNING_MOVE, "congratulation message!")
		# otherwise, just returns (NORMAL_MOVE, "")
		return NORMAL_MOVE, ""


	def getDataSize(self):
		"""
		Returns the size of the datas send by getData
		(for example sizes of arrays, so that the arrays could be allocated before calling getData)
		"""
		#
		# insert your code here...
		#
		return ""



	def getData(self):
		"""
		Return the datas of the game (when ask with the GET_GAME_DATA message)
		"""
		#
		# insert your code here...
		#
		return ""




	def getNextPlayer(self):
		"""
		Change the player who plays

		Returns the next player (but do not update self._whoPlays)
		"""
		#
		# insert your code here...
		#
		return 1 - self._whoPlays       # in a tour-by-tour game, it's the opponent to play


""