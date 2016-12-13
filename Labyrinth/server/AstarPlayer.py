"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire, J. Brajard
Licence: GPL
Status: still in dev...

File: playRandomPlayer.py
	Contains the class playRandomPlayer
	-> defines a dummy player that play randomly every time (but do not loose)
"""

from CGS.Player import TrainingPlayer
from random import choice, randint
from .Constants import MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP, DO_NOTHING
from .Constants import ROTATE_COLUMN_DOWN, ROTATE_COLUMN_UP, ROTATE_LINE_LEFT, ROTATE_LINE_RIGHT, ROTATE_ENERGY
from .Constants import Ddx, Ddy

boolConv = {'true': True, 'false': False}


class AstarPlayer(TrainingPlayer):

	def __init__(self, **options):
		super().__init__('Play_Random')



	def neighbours(self,x,y):
		"""
		:param x: coordinate of a point
		:param y: coordinate of a point
		:return: list of neighbours of the point (x,y)
		"""
		return [ ((x + Ddx[move_type]) % self.game.L, (y + Ddy[move_type]) % self.game.H)\
				for move_type in (MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT)]

	def playMove(self):
		"""
		Plays the move -> here a random move
		Returns the move (string %d %d)
		"""
		# get our player number
		us = 0 if (self.game.players[0] is self) else 1

		# build the grid of distances
		delta = [list((-1,) * self.game.H) for _ in range(self.game.L)]
		delta[self.game.treasure[0]][self.game.treasure[1]] = 0

		loop = True

		#Loop if data are style to explore
		while loop:
			loop = False
			for x in range(self.game.L):
				for y in range(self.game.H):
					if delta[x][y] >= 0:
						for (xn,yn) in self.neighbours(x,y):
							if self.game.lab[xn][yn] and delta[xn][yn] == -1:
								loop = True
								delta[xn][yn] = delta[x][y]+1

		#Our position
		xp,yp = self.game.playerPos[us]
		moves = dict()
		#Find the best move
		for move_type in (MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT):
			x, y = self.game.playerPos[us]
			x = (x + Ddx[move_type]) % self.game.L
			y = (y + Ddy[move_type]) % self.game.H

			if self.game.lab[x][y]:
				moves[move_type] = delta[x][y]

		if moves:
			bestmove = min(moves, key=moves.get)
			return "%d 0" % bestmove
		else:
			self.game.sendComment(self, "I am blocked... I cannot move...")
			return "%d 0" % DO_NOTHING