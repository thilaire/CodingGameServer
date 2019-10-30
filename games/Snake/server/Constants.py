"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire, T. Gautier
Licence: GPL

File: Constants.py
	Contains the constants of the game Snake
	-> defines the constants used for the client communication

Copyright 2019 T. Hilaire, T. Gautier
"""

# constants defining a move
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# simple dictionary of x and y offsets
Ddx = {NORTH: 0, SOUTH: 0, EAST: -1, WEST: 1}
Ddy = {NORTH: -1, SOUTH: 1, EAST: 0, WEST: 0}


