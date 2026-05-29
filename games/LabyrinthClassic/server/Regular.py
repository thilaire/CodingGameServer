"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire
Licence: GPL

File: Basic.py
	Contains the class Basic
	-> defines a player that look at every possible move and keep the best one (1st level depth)

Copyright 2016-2017 T. Hilaire, J. Brajard
"""

from CGSserver.Player import TrainingPlayer
from itertools import product
from random import shuffle
from copy import deepcopy
from operator import itemgetter
from math import sqrt
from CGSserver.Player import TrainingPlayer
from random import choice, randint
from .Constants import INSERT_COLUMN_BOTTOM, INSERT_COLUMN_TOP, INSERT_LINE_LEFT, INSERT_LINE_RIGHT, OPPOSITE, MAX_ITEM
from .Laby import L1dist


class RegularPlayer(TrainingPlayer):
	"""
	class BasicPlayer that create a Basic player trainer
	"""

	def __init__(self, **_):
		super().__init__('Regular')


	def playMove(self):
		"""
		Plays the move -> here a random move
		Returns the move (string %d %d %d %d %d)
		"""
		moves = {}
		# get our player number
		us = 0 if (self.game.players[0] is self) else 1

		# generate the list of possible (numbers, insert)
		ni = list(product(range(1, self.game.L-1, 2), [INSERT_COLUMN_BOTTOM, INSERT_COLUMN_TOP])) + \
			  list(product(range(1, self.game.H-1, 2), [INSERT_LINE_LEFT, INSERT_LINE_RIGHT]))
		# remove the last move
		lastInsert, lastNumber = self.game.lastInsert
		try:
			ni.remove((lastNumber, OPPOSITE[lastInsert]))
		except ValueError:
			pass
		# add all the possible rotations, and shuffle
		nir = list(product(ni, range(0, 4)))
		shuffle(nir)

		# iter over all the possinilities
		for (number, insert), rotate in nir:
			# copy the labyrinth and play the move
			lab = deepcopy(self.game._lab)
			playerPos = self.game._playerPos.copy()
			lab.extraTile.rotate(rotate)
			lab.insertExtraTile(insert=insert, number=number, playerPos=playerPos)

			nbI = 0
			lpos = ""
			l1d = 0
			lab.reachable(*playerPos[self.game._whoPlays])
			lastPos = playerPos[self.game._whoPlays]
			while True:
				# search for the next item
				nextItem = self.game._playerItem[self.game._whoPlays] + (-nbI if self.game._whoPlays else +nbI)
				if nextItem == (0 if self.game._whoPlays else MAX_ITEM+1):
					nbI = 100
					break
				itemPos = [(x, y) for x in range(self.game.L) for y in range(self.game.H) if lab[x, y].item == nextItem]
				xitem, yitem = itemPos[0] if itemPos else playerPos[self.game._whoPlays]

				#try to reach the next item

				if lab[xitem, yitem].reachable and (l1d + L1dist((xitem, yitem), lastPos)) < 10:
					nbI += 1
					l1d += L1dist((xitem, yitem), playerPos[self.game._whoPlays])
					lpos += "%d %d " % (xitem, yitem)
					lastPos = xitem, yitem
					if nbI > 9:
						break
				else:
					break

			if nbI > 0:
				moves["%d %d %d " % (insert, number, rotate)+lpos] = nbI


		# if not, move to the reachable tile that is the closest to the item to reach
		pos = [(x, y) for x in range(self.game.L) for y in range(self.game.H) if lab[x, y].reachable]  # list of reachable points
		dist = list(map(lambda p: sqrt((p[0] - xitem) ** 2 + (p[1] - yitem) ** 2), pos))  # list of distance
		x, y = pos[min(enumerate(dist), key=itemgetter(1))[0]]		# find the index of the minimum distance
		moves[ "%d %d %d %d %d" % (insert, number, rotate, x, y)] = 0

		#find the best move
		bestMove = max(moves, key=moves.get)
		if moves[bestMove] == 1:
			self.game.sendComment(self, "I found another item !")
		elif moves[bestMove] > 1:
			self.game.sendComment(self, "I found %d items in one move !!!" % moves[bestMove])
		return bestMove

