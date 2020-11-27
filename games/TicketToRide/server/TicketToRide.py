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

from re import compile
from colorama import Fore
from random import shuffle
from CGSserver.Constants import NORMAL_MOVE, WINNING_MOVE, LOSING_MOVE
from CGSserver.Game import Game
from .DoNothingPlayer import DoNothingPlayer
from .Map import Map
from .Cards import Deck, strCards
from .Constants import textColors, MULTICOLOR, PURPLE


regClaimRoute = compile(r"^\s*1\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)")   # regex to parse a "1 %d %d %d %d"
regDrawBlindCard = compile(r"^\s*2")                                # regex to parse "2"
regDrawCard = compile(r"^\s*3\s+(\d+)")                             # regex to parse "3 %d"
regDrawObjectives = compile(r"^\s*4")                               # regex to parse "4"
regChooseObjectives = compile(r"^\s*5\s+(\d+)\s+(\d+)\s+(\d+)")     # regex to parse "5 %d %d %d"


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
	- _theMap: Map object (only used to build the object or get initial data)
	- _deck: the train cards deck (a Deck object, with all the methods to get cards, shuffle, etc.)
	- _cards: cards[pl] is the list of cards of the player pl. _cards[pl][i] gives how many cards of colors i the player pl has
	- _score, _nbWagons: a 2-element list with the score and number of wagons for each player
	- _objectivesDeck: list of objectives cards in the deck (an objective card is 3-uplet city1;city2;points)
	- _objectives: list of objectives of each player (a 2-element list)
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

		# set the seed
		self._setseed(options)

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
		self._objectivesDeck = self._theMap.objectives      # get a copy of the list of objectives
		shuffle(self._objectivesDeck)
		self._objectives = [[], []]
		self._objDrawn = []     # list of drawn objectives (3 objectives kept between drawObjective and chooseObjective)

		self._shouldTakeAnotherCard = False      # True if the player has taken a card and MUST take another one

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
				lines.append("\t\t Cards (%2d): " % sum(self._cards[i]) + " ".join(strCards(c, self._cards[i][c]) for c in range(1, MULTICOLOR+1)))
			else:
				lines.append("\t\t Cards (%2d)" % sum(self._cards[i]))

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
		pl = self._whoPlays
		# parse for the different moves
		claimRoute = regClaimRoute.match(move)
		drawBlindCard = regDrawBlindCard.match(move)
		drawCard = regDrawCard.match(move)
		drawObjectives = regDrawObjectives.match(move)
		chooseObjectives = regChooseObjectives.match(move)
		# if the last move was drawObjectives, then this move MUST be chooseObjectives
		if self._objDrawn and not chooseObjectives:
			return LOSING_MOVE, "a `draw objectives` move must be followed by a `choose objectives` move"
		# if the last move was drawCard and the card was not a Locomotive, then this move MUST be drawCard or drawBlindCard
		if self._shouldTakeAnotherCard and not (drawCard or drawBlindCard):
			return LOSING_MOVE, "a `draw card` or `draw blind card` must be followed by a `draw card` " \
			                    "or `draw blind card` (except for Locomotive taken face up)"

		# Claim a route
		if claimRoute:
			# TODO:
			# TODO: deal with the end of the game (last turn when one player has < 3 wagons)
			return NORMAL_MOVE, ""

		# Draw a blind card
		elif drawBlindCard:
			# get a card from the deck (end of the game if the deck is empty)
			try:
				draw = self._deck.drawBlind()
				self._cards[pl][draw] += 1
			except ValueError:
				return (LOSING_MOVE if sum(self._cards[pl]) >= sum(self._cards[1-pl]) else WINNING_MOVE),\
					"No more cards in the deck !!"
			self._shouldTakeAnotherCard = not self._shouldTakeAnotherCard     # need/no need to take another card
			deck = " ".join(str(c) for c in self._deck.faceUp)
			# send:
			# - to the player: card drawn
			# - to the opponent: if the player replay
			return NORMAL_MOVE, str(draw), ("1 " if self._shouldTakeAnotherCard else "0 ")

		# Draw a train card
		elif drawCard:
			# get a card from the face up cards (end of the game if the deck is empty, or the card doesn't exist)
			# get the card position
			card = int(drawCard.group(1))
			try:
				nC = self._deck.faceUp.index(card)
			except ValueError:
				return LOSING_MOVE, "The card doesn't exist in the face up cards"
			# replace it by one in the deck
			try:
				if self._deck.drawFaceUpCard(nC):
					self.sendComment(self.playerWhoPlays, "Choo choo, three locomotives... New face up cards !")
			except ValueError:
				return (LOSING_MOVE if sum(self._cards[pl]) >= sum(
					self._cards[1 - pl]) else WINNING_MOVE), "No more cards in the deck !!"
			# check if the player can take a Locomotive
			if self._shouldTakeAnotherCard and card == MULTICOLOR:
				return LOSING_MOVE, "You cannot take a Locomotive as 2nd drawn card"
			# add it in the hand
			self._cards[pl][card] += 1
			# if it's not a Locomotive, the player MUST take another one
			if card != MULTICOLOR:
				self._shouldTakeAnotherCard = not self._shouldTakeAnotherCard
			deck = " ".join(str(c) for c in self._deck.faceUp)
			# send:
			# - to the player: the deck
			# - to the opponent: if the player replay, the card taken and the deck
			return NORMAL_MOVE, deck, ("1 " if self._shouldTakeAnotherCard else "0 ") + str(card) + " " + deck

		# Draw an objective card
		elif drawObjectives:
			if not self._objectivesDeck:
				return (LOSING_MOVE if len(self._objectives[pl]) > len(self._objectives[1 - pl]) else WINNING_MOVE),\
					"No more available objective cards !!"
			self._objDrawn = [self._objectivesDeck.pop() for _ in range(3)]
			return NORMAL_MOVE, " ".join("%d %d %d" % c for c in self._objDrawn), ""

		# Choose an objective card
		elif chooseObjectives:
			objs = [int(chooseObjectives.group(1)), int(chooseObjectives.group(2)), int(chooseObjectives.group(3))]
			# check if at least one objective is taken
			if sum([1 if o else 0 for o in objs]) == 0:
				return LOSING_MOVE, "None objective has been kept"
			# TODO: check that at least 2 objectives are kept for the 1st move
			# put the chosen objectives in the player hand, or back in the objective deck
			for i in range(3):
				if objs[i]:
					self._objectives[pl].append(self._objDrawn[i])
				else:
					self._objectivesDeck.append(self._objDrawn[i])
			self._objDrawn = []
			return NORMAL_MOVE, str(len([o for o in objs if o]))  # returns the number of chosen objectives


		return LOSING_MOVE, "The move is not in correct !"



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

		# send the cities, the face-up cards and the player cards
		return self._theMap.data + " " + " ".join(str(c) for c in self._deck.faceUp) + " " + " ".join(cards)


	def getNextPlayer(self):
		"""
		Change the player who plays

		Returns the next player (but do not update self._whoPlays)
		"""
		# in case of `draw objective` move, the player replay
		return self._whoPlays if (self._shouldTakeAnotherCard or self._objDrawn) else 1 - self._whoPlays

	def faceUpCards(self):
		"""Return the list of face up cards (for the bots)"""
		return list(self._deck.faceUp)