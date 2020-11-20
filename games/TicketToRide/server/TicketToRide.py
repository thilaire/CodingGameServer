"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire
Licence: GPL

File: TicketToRide.py
	Contains the class TicketToRide
	-> defines the Ticket To Ride game (its rules, moves, etc.)

Copyright 2020 T. Hilaire
"""

from colorama import Fore
from CGSserver.Constants import NORMAL_MOVE, WINNING_MOVE, LOSING_MOVE
from CGSserver.Game import Game
from .DoNothingPlayer import DoNothingPlayer
from .Map import Map
from .Cards import Deck, strCards
from .Constants import textColors, MULTICOLOR, PURPLE




class TicketToRide(Game):
	"""
	class TicketToRide (Ticket To Ride)

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

	# possible maps
	maps = {m: Map(m) for m in ('USA',)}


	def __init__(self, player1, player2, **options):
		"""
		Create a game
		:param player1: 1st Player
		:param player2: 2nd Player
		:param options: dictionary of options (the options 'seed' and 'timeout' are managed by the Game class)
		"""
		# get the map
		if 'map' in options:
			try:
				self._theMap = self.maps[options['map']]
			except KeyError:
				raise ValueError(
					"The option `map` is incorrect (%s instead of being in [%s])"
					% (options['map'], list(self.maps.keys())))
		else:
			self._theMap = self.maps['USA']

		# initialize the deck and give 4 cards per player
		self._deck = Deck()                 # deck of train cards
		self._cards = [[0]*10, [0]*10]        # self._cards[pl][c] gives how many cards c the player pl has
		for pl in range(2):
			for _ in range(4):
				self._cards[pl][self._deck.drawBlind()] += 1

		# score and wagons
		self._score = [0, 0]
		self._nbWagons = [45, 45]

		# objectives
		self._objectives = [[], []]

		# call the superclass constructor (only at the end, because the superclass constructor launches
		# the players and they will immediately requires some Labyrinth's properties)
		super().__init__(player1, player2, **options)

		self.logger.debug("FaceUp= " + " ".join(str(c) for c in self._deck.faceUp))
		self.logger.debug("Init cards = " + str(self._cards))


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
		colors = [Fore.BLUE, Fore.RED]
		lines = ["\t\tCards: " + " ".join(strCards(c, c) for c in self._deck.faceUp) + "\n"]
		for i, pl in enumerate(self._players):
			br = "[]" if self._whoPlays == i else "  "
			lines.append("\t\t" + br[0] + colors[i] + "Player " + str(i + 1) + ": " + Fore.RESET + pl.name + br[1])
			lines.append("\t\t Score: %3d \t Wagons: %2d \t Objectives: %d" %
			             (self._score[i], self._nbWagons[i], len(self._objectives[i])))
			if i == self._whoPlays:
				lines.append("\t\t Cards: " + " ".join(strCards(c, self._cards[i][c]) for c in range(1, MULTICOLOR+1)))

			lines.append("\n")

		return "\n".join(lines)


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
		# send the number of cities and the number of tracks
		return "%d %d" % (self._theMap.nbCities, self._theMap.nbTracks)



	def getData(self):
		"""
		Return the datas of the game (when ask with the GET_GAME_DATA message)
		ie the map data, the face up cards and the 4 initial cards (for each player)
		"""
		# get the list of the cards
		pl = self._whoPlays
		cards = []
		for i, c in enumerate(self._cards[pl]):
			if c > 0:
				for _ in range(c):
					cards.append(str(i))
		# send the cities and the deck

		return self._theMap.data + " " + " ".join(str(c) for c in self._deck.faceUp) + " " + " ".join(cards)


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