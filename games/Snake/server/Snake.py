"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire, T. Gautier
Licence: GPL

File: Snake.py
	Contains the class Snake
	-> defines the Snake game (its rules, moves, etc.)

Copyright 2019 T. Hilaire, T. Gautier
"""

from random import randint
from server.Constants import NORMAL_MOVE, WINNING_MOVE, LOSING_MOVE
from .Constants import NORTH, SOUTH, EAST, WEST, Ddx, Ddy
from server.Game import Game

# import here your training players
from .StupidPlayer import StupidPlayer



class Box:
	"""
	the arena is an array of Box (ie integers)
	arena[x][y] indicates what is at position x,y
	- bits 0 to 3 are for the wall (arena[x][y] & (1<<DIR) -> tells if there is a wall in direction DIR)
	- bits 7 and 8 are for the players 0 and 1
	the class Box just encapsulates this
	"""
	def __init__(self):
		self._v = 0
	def setWall(self, direction):
		self._v |= self._v | (1 << direction)
	def getWall(self, direction):
		return bool(self._v & (1 << direction))
	def setNoone(self):
		self._v &= 63
	def setPlayer(self, nPlayer):
		self._v |= 1 << (7+nPlayer)
	def getPlayer(self):
		return {0: None, 1: 0, 2: 1}[self._v >> 7]

	def __repr__(self):
		return bin(self._v)


def createGame(L, H, difficulty):
	"""create a game
	Returns an arena (array of integers) and a set of walls"""
	# create a L*H array of 0)
	arena = [[Box() for _ in range(H)] for _ in range(L)]
	walls = []
	# put walls around the arena to bound it
	for x in range(L):
		arena[x][0].setWall(NORTH)
		arena[x][-1].setWall(SOUTH)
	for y in range(H):
		arena[0][y].setWall(WEST)
		arena[-1][y].setWall(EAST)
	# fill with walls according to the difficulty
	nbWalls = [0, L*H//5, L*H//2, L*H][difficulty]
	for i in range(nbWalls):
		x = randint(0, L-1)
		y = randint(0, H-1)
		direction = randint(0, 3)
		arena[x][y].setWall(direction)     # no need to check if the wall already exists
		walls.append((x, y, x + Ddx[direction], y + Ddy[direction]))

	return arena, set(walls)

class Snake(Game):
	"""
	class Snake

	Inherits from Game
	- _players: tuple of the two players
	- _logger: logger to use to log infos, debug, ...
	- _name: name of the game
	- _whoPlays: number of the player who should play now (0 or 1)
	- _waitingPlayer: Event used to wait for the players
	- _lastMove, _last_return_code: string and returning code corresponding to the last move

	And some properties
	- _game: array (list of list of integers) representing the game
	- _walls: list of walls (only used to send to the players)
	- _L,_H: length and height of the area
	- playerPos: list of the coordinates (itself a list) of the two players
	"""

	# dictionary of the possible training Players (name-> class)
	type_dict = {"STUPID_PLAYER": StupidPlayer}



	def __init__(self, player1, player2, **options):
		"""
		Create a game
		:param player1: 1st Player
		:param player2: 2nd Player
		:param options: dictionary of options (the options 'seed' and 'timeout' are managed by the Game class)
		"""

		# random Labyrinth
		totalSize = randint(40, 60)  # sX + sY is randomly in [30,60]
		self._L = randint(20, 40)
		self._H = totalSize - self._L
		self._L, self._H = max(self._L, self._H), min(self._L, self._H)   # L is greater than H
		self._arena, self._walls = createGame(self._L, self._H, int(options.get("difficulty", 2)))

		#TODO: set the players

		# call the superclass constructor (only at the end, because the superclass constructor launches
		# the players and they will immediately requires some Labyrinth's properties)
		super().__init__(player1, player2, **options)



	def HTMLrepr(self):
		"""Returns an HTML representation of your game"""
		# this, or something you want...
		return "<A href='/game/%s'>%s</A>" % (self.name, self.name)

	# def getDictInformations(self):
	# 	"""
	# 	Returns a dictionary for HTML display
	# 	:return:
	# 	"""
	# 	conv = Ansi2HTMLConverter()
	# 	html = conv.convert(str(self))
	# 	#TODO:
	# 	return {'content': html}


	def __str__(self):
		"""
		Convert a Game into string (to be send to clients, and display)
		"""
		lines = []
		for y in range(self._H):
			lines1 = []
			lines2 = []
			for x in range(self._L):
				lines1.append('+-' if self._arena[x][y].getWall(NORTH) else '+ ')
				pl = {None: ' ', 0: 'X', 1: 'O'}[self._arena[x][y].getPlayer()]
				lines2.append(('|' if self._arena[x][y].getWall(WEST) else ' ') + pl)
			lines1.append('+')
			lines2.append('|' if self._arena[x][y].getWall(EAST) else ' ')
			lines.append("".join(lines1))
			lines.append("".join(lines2))
		lines.append("".join(('+-' if self._arena[x][-1].getWall(SOUTH) else '+ ') for x in range(self._L))+"+")

		#TODO: add colors
		#TODO: add player names
		#TODO: add counter (length of the snakes?)
		#TODO: add gameName, etc.
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
		return "%d %d %d" % (self._L, self._H, len(self._walls))



	def getData(self):
		"""
		Return the datas of the game (when ask with the GET_GAME_DATA message)
		ie the list of positions of walls
		"""
		return " ".join("%d %d %d %d" % wall for wall in self._walls)



#
# 	def getNextPlayer(self):
# 		"""
# 		Change the player who plays
#
# 		Returns the next player (but do not update self._whoPlays)
# 		"""
# 		#
# 		# insert your code here...
# 		#
# 		return 1 - self._whoPlays       # in a tour-by-tour game, it's the opponent to play
#
#
# ""