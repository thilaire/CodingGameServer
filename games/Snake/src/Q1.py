"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire, T. Gautier
Licence: GPL

File: snakeAPI.py
	A python version of the snakeAPI

Copyright 2019 T. Hilaire, T. Gautier
"""

from snakeAPI import SnakeAPI

import random

client = SnakeAPI(5)

client.connectToServer("localhost", 1234, "PY_TEST_" + str(random.randint(0, 1000)))

gameName, sizeX, sizeY, nbWalls = client.waitForSnakeGame("SUPER_PLAYER difficulty=2 timeout=100 seed=123 start=0")

walls, player = client.getSnakeArena()

ret = 0
while ret == 0:
	client.printArena()

	if player == 1:
		move, ret = client.getMove()
	else:
		move = input("It's your turn to play (0:NORTH, 1:EAST, 2:SOUTH, 3:WEST)")
		ret = client.sendMove("%d" % int(move))
	player = 0 if (player == 1) else 1

if (player == 0 and ret == 1) or (player == 1 and ret == -1):
	print("Unfortunately, the opponent wins")
else:
	print("Héhé, I win!!")

client.closeConnection()