"""
This file is a template for a new Game in CGS

The two main methods to fill in are:
	- the __init__ to build the game (you put all the intern data here)
	- the updateMove, to check if a move is legal, to play it (and change the intern state of the game),
	and returns if the move is legal or not

Then, you should also fill:
	- the __str__ method, that build the string returns to the player to display the game
	- the getDataSize and getData methods, for the client to know the initial state of the game
	- the getDictInformations, to display the game on webpages


"""

from CGSserver.Constants import NORMAL_MOVE, WINNING_MOVE, LOSING_MOVE
from CGSserver.Game import Game
from random import seed

from .SDGameHandler import SDGameHandler
# import here your training players
from .SplendorVegetablePlayer import SplendorVegetablePlayer


class SplendorDuel(Game):
	"""
	class SplendorDuel

	Inherits from Game
	- _players: tuple of the two players
	- _logger: logger to use to log infos, debug, ...
	- _name: name of the game
	- _whoPlays: number of the player who should play now (0 or 1)
	- _waitingPlayer: Event used to wait for the players
	- _lastMove, _last_return_code: string and returning code corresponding to the last move

	Add here your own properties
	- ...
	"""

	# dictionary of the possible training Players (name-> class)
	type_dict = {"MY_TRAINING_PLAYER": SplendorVegetablePlayer}

	# TODO: privilege scroll management (memo: redistribute, 3-token capture, take from opponent, use one)
	# TODO: token management

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


		# Each player may or may not own one or some:
		#	-bonus(es)
		#	-prestige point(s) (<20 otherwise it's a win)
		#	-crown(s) (<10, same reason)
		#	-Jewel card(s) (it's the standard cards, =/= the 4 crown cards)
		#		(side note: <10 prestige point per gemstone (otherwise, win))
		#	-royal card(s) (you can obtain one whenever you hit 3 and 6 crowns)
		#	-gemstone (token(s))
		#	-perl (token(s))
		#	-gold (token(s))
		#	-sleep (token) (they don't, but you can listen to ST, I'm just a fooling around a little :) )
		#	-0 to 3 privilege scroll(s)
		# I believe that's it?

		# Player inventories are managed in the game handler (w/ all the things above)


		# To use when distributing the gemstone tokens on the board
		# get a seed if the seed is not given; seed the random numbers generator
		if 'seed' in options:
			seed(int(options['seed']))
			self.gameHandler = SDGameHandler(int(options["seed"])) #I guess I don't need to implement the seed in the handler anymore??



		# Every turn, you have an optional move/action, then a mandatory one.
		# You may skip the optional moves (duh)
		#	optional (choose among the following):
		#		-Use a privilege scroll to take a gemstone or a pearl (not a gold token though) (privilege scroll required, obviously)
		#
		#		-Redistribute the tokens. As a consequence, your opponent gets a privilege scroll.
		#		 /!\ If you have three privilege scrolls, yours gets taken away for their profit /!\
		#
		#	mandatory (choose one of the three):
		#		-Take 1 to 3 gemstone/pearl tokens from the board
		#			conditions: -Only vertical, horizontal and diagonal
		#						-No gold token
		#						-No space between two tokens
		#						-If you choose three identical gemstones or two pearls in one move,
		#						your opponent gets a privilege scroll. Same goes here:
		#						/!\ If you have three privilege scrolls, yours gets taken away for their profit /!\
		#
		#		-Book a Jewel card (the opponent isn't supposed to see it anymore,
		#		though they can memorize it (not really relevant to this computer version))
		#			conditions:	-You either take one from the pyramid or one from the three stacks (level 1, 2 or 3)
		#						-You have to take a gold token from the board.
		#						-Illegal if there isn't one anymore
		#						-Illegal if you already have three booked cards
		#						-You do not need to buy any of the cards you booked
		#
		#		-Buy a Jewel card
		#			conditions:	-You need enough gemstones to buy one card
		#							e.g. a card requires 2 rubies and 3 blue sapphires.
		#							You then need that amount of tokens, minus the ones from the Jewel cards you
		#							already own. So if you have two blue sapphire tokens, a blue sapphire cards and two
		#							ruby tokens, you can buy that card. You will lose the tokens, not the Jewel
		#							cards, and get this card in your inventory.
		#						-Gold token can substitute any other gemstone or pearl.
		#							e.g. a card requires two pearls and two obsidian tokens.
		#							You own a pearl, a gold, two obsidian tokens and an obsidian Jewel card.
		#							You can then buy the card. You will lose your pearl, your gold and an obsidian token
		#
		# 	Once you have 3 or 6 crowns, you have to take a royal card, but it doesn't account
		# 	for a mandatory nor an optional move.
		#
		#
		# Probably one method per move?

		#
		#	Jewel cards have different levels: one, two, and three.
		#	We display a pyramid of them. 5 cards are level 1, 4 cards are level 2, 3 cards are level 3.



		# As a player, what's useful to know? (thinking to make an ascii representation for players)
		# What's on the pyramid
		# How many Prestige points both have (player and opponent)
		# How many crowns
		# How many prestige points in a single color your opponent has
		#	therefore in every color...
		# how many privilege scrolls both have
		# how many tokens both have
		# how many Jewel cards per color both have

		#TODO: ILLEGAL TO HAVE MORE THAN TEN GEMS PER PLAYER
		#e.g. Let a player w/ 10 gems who chooses to to take tokens on the board.
		#In one turn, they have to chose which token they choose + which token they give back to the "bank"?
		#N.B. the "bank" represents the tokens which are going to be redistributed on the board when needed.

		# call the superclass constructor (only at the end, because the superclass constructor launches
		# the players and they will immediately require some Labyrinth's properties)
		##side note: there's no labyrinth here, right?
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
		Return a tuple (move_code, msg) OR (move_code, msg, msgOppenent), where
		- move_code: (integer) 0 if the game continues after this move, >0 if it's a winning move, -1 otherwise (illegal move)
		- msg: a message to send to the players, explaining why the game is ending, it may contain data
		- msgOpponnent: (OPTIONAL) a message sent to the opponent, IF the opponent should not receive the same data
		"""
		# parse the move and check if it's in correct form
		# returns the tuple (LOOSING_MOVE, "The move is not in correct form  !") if not valid




		# check the move
			# -> need to define how `move`'s going to look like w/ regex for instance.
		# returns (LOOSING_MOVE, "explanations....") if not valid (give the full reason why it is not valid)

		optional = str()

		# # check for optional moves
		# match optional:
		# #	either nothing
		# 	case NO_OPTIONAL_MOVE:
		# 		pass
		# #	either use of a privilege scroll to take a token on the board:
		# 	case TAKE_TOKEN:
		# 		self.gameHandler.addToInventory(self._whoPlays, PRIVILEGE, -1)
		# 		self.gameHandler.addToInventory
		# #	either redistribute the tokens on the board
		# 	case REDISTRIBUTE:
		# 		pass




		# if it's recognised, do the appropriate actions, use the right methods

		# move the player
		# update the intern data
		# use self._whoPlays to get who plays (0 or 1)

		# if won, returns the tuple (WINNING_MOVE, "congratulation message!")
		# otherwise, just returns (NORMAL_MOVE, "")
		# an optional 3rd parameter is possible (if the message is used to send data)
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



	def getData(self, player):
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
