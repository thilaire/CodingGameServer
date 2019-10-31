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

from random import randint, seed
from server.Constants import NORMAL_MOVE, WINNING_MOVE, LOSING_MOVE
from .Constants import NORTH, SOUTH, EAST, WEST, Ddx, Ddy
from server.Game import Game
from colorama import Fore
from re import compile
from itertools import product

# import here your training players
from .RandomPlayer import RandomPlayer

import logging
logger = logging.getLogger("Snake")  # general logger ('root')

regd = compile(r"(\d+)")  # regex to parse a "%d" string


class Arena:
	"""
	the arena is an array of integers

	In intern, for each box x,y of the arean
	- bits 0 to 3 are for the wall (arena[x][y] & (1<<DIR) -> tells if there is a wall in direction DIR)
	- bits 7 and 8 are for the players 0 and 1
	the class Box just encapsulates this
	"""
	def __init__(self, L, H, difficulty):
		"""create a game
		Returns an arena (array of integers) and a set of walls"""
		self._L = L
		self._H = H
		# create a L*H array of 0)
		self._array = [[0 for _ in range(H)] for _ in range(L)]
		self._walls = []
		# fill with random walls according to the difficulty
		nbWalls = [0, L*H//4, L*H//2, L*H][difficulty]
		for i in range(nbWalls):
			x = randint(0, L-1)
			y = randint(0, H-1)
			direction = randint(0, 3)
			self._setWall(x, y, direction)     # no need to check if the wall already exists
			self._setWall(x + Ddx[direction], y + Ddy[direction], (direction+2)%4)    # wall in the adjacent box
			self._walls.append((x, y, x + Ddx[direction], y + Ddy[direction]))
		# remove walls around the start position (just in case)
		for x, y in [(2, H//2), (L-3, H//2)]:
			for dx, dy in product(range(-1,2), range(-1,2)):
				self._removeWall(x+dx, y+dy)
		# put walls around the arena to bound it
		for x in range(L):
			self._setWall(x, 0, NORTH)
			self._setWall(x, -1, SOUTH)
		for y in range(H):
			self._setWall(0, y, WEST)
			self._setWall(-1, y, EAST)


	@property
	def walls(self):
		return self._walls

	def _setWall(self, x, y, direction):
		if -1 <= x < self._L and -1 <= y < self._H:
			self._array[x][y] |= 1 << direction

	def _removeWall(self, x, y):
		self._array[x][y] &= 128+64

	def getWall(self, x, y, direction):
		return bool(self._array[x][y] & (1 << direction))

	def setNoone(self, x, y):
		self._array[x][y] &= 63

	def setPlayer(self, x, y, nPlayer):
		self._array[x][y] |= 1 << (6+nPlayer)

	def getPlayer(self, x, y):
		return {0: None, 1: 0, 2: 1}[self._array[x][y] >> 6]


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
	- _arena: (Arena) array representing the game
	- _L,_H: length and height of the area
	- playerPos: list of the coordinates (itself a list) of the two players
	"""

	# dictionary of the possible training Players (name-> class)
	type_dict = {"RANDOM_PLAYER": RandomPlayer}

	def __init__(self, player1, player2, **options):
		"""
		Create a game
		:param player1: 1st Player
		:param player2: 2nd Player
		:param options: dictionary of options (the options 'seed' and 'timeout' are managed by the Game class)
		"""

		# get a seed if the seed is not given; seed the random numbers generator
		if 'seed' in options:
			seed(int(options['seed']))

		# random arena
		totalSize = randint(40, 60)  # sX + sY is randomly in [30,60]
		self.L = randint(20, 40)
		self.H = totalSize - self.L
		self.L, self.H = max(self.L, self.H), min(self.L, self.H)   # L is greater than H
		self.arena = Arena(self.L, self.H, int(options.get("difficulty", 1)))

		# players positions (list of positions, firsst is the head)
		self.playerPos = [[(2, self.H // 2)], [(self.L - 3, self.H // 2)]]

		self.arena.setPlayer(2, self.H // 2, 0)
		self.arena.setPlayer(self.L - 3, self.H // 2, 1)

		# counter (one per player), used to know when the snake grows
		self.counter = [0,0]

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
		# create the lines
		lines = []
		for y in range(self.H):
			lines1 = []
			lines2 = []
			for x in range(self.L):
				# 1st line (with NORTH wall)
				lines1.append('+-' if self.arena.getWall(x, y, NORTH) else '+ ')
				# character of the x,y box
				pl = self.arena.getPlayer(x, y)
				strPl = {None: ' ', 0: 'M', 1: 'O'}[pl]
				if pl is not None and (x, y) == self.playerPos[pl][0]:
					strPl = (Fore.GREEN if pl else Fore.RED) + strPl + Fore.RESET
				# 2nd line (with WEST wall)
				lines2.append(('|' if self.arena.getWall(x, y, WEST) else ' ') + strPl)
			# add end of the line (EAST walls)
			lines1.append('+')
			lines2.append('|' if self.arena.getWall(-1, y, EAST) else ' ')
			lines.append("".join(lines1))
			lines.append("".join(lines2))
		# end the last walls in the SOUTH
		lines.append("".join(('+-' if self.arena.getWall(x, -1, SOUTH) else '+ ') for x in range(self.L)) + "+")

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
		result = regd.match(move)
		# check if the data receive is valid
		if result is None:
			return LOSING_MOVE, "The move is not in correct form ('%d') !"

		# get the type and the value
		direction = int(result.group(1))
		# check the possible values
		if not (NORTH <= direction <= WEST):
			return LOSING_MOVE, "The direction is not valid (should be between 0 and 3!"

		# move the player
		pl = self._whoPlays
		# head position and new position
		hx, hy = self.playerPos[pl][0]
		nx = hx + Ddx[direction]
		ny = hy + Ddy[direction]
		# check if there is a wall and if the new position is free
		if self.arena.getWall(hx, hy, direction):
			return LOSING_MOVE, "The move make the snakes goes into a wall"
		if self.arena.getPlayer(nx, ny) is not None:
			return LOSING_MOVE, "The move make the snakes collides..."
		# the snake move
		self.arena.setPlayer(nx, ny, pl)
		self.playerPos[pl].insert(0, (nx, ny))
		# and it may grow or not
		if self.counter[pl]%10 != 0:
			qx, qy = self.playerPos[pl].pop()
			self.arena.setNoone(qx, qy)
		# increase the counter
		self.counter[pl] = (self.counter[pl] + 1) % 10

		logger.debug("self._playerPos=%s",self.playerPos)

		return NORMAL_MOVE, ""


	def getDataSize(self):
		"""
		Returns the size of the datas send by getData
		(for example sizes of arrays, so that the arrays could be allocated before calling getData)
		"""
		return "%d %d %d" % (self.L, self.H, len(self.arena.walls))



	def getData(self):
		"""
		Return the datas of the game (when ask with the GET_GAME_DATA message)
		ie the list of positions of walls
		"""
		return " ".join("%d %d %d %d" % wall for wall in self.arena.walls)



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