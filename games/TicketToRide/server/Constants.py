"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire
Licence: GPL

File: Constants.py
	Contains the constants of the game Ticket To Ride
	-> defines the constants used for the client communication

Copyright 2020 T. Hilaire
"""


from colorama import Fore, Back

# colors
colors = {
	'None': 0,
	'Purple': 1,
	'White': 2,
	'Blue': 3,
	'Yellow': 4,
	'Orange': 5,
	'Black': 6,
	'Red': 7,
	'Green': 8,
	'Multicolor': 9     # used for the locomotive card (joker) or for a track that can accept any color
}

NONE = 0
PURPLE = 1
WHITE = 2
BLUE = 3
YELLOW = 4
ORANGE = 5
BLACK = 6
RED = 7
GREEN = 8
MULTICOLOR = 9

textColors = [
	Fore.RESET, Fore.MAGENTA, Fore.BLACK, Fore.BLUE, Fore.LIGHTYELLOW_EX,
	Fore.YELLOW, Fore.WHITE, Fore.RED, Fore.GREEN, Fore.WHITE
]

# score for the tracks
Scores = [0, 1, 2, 4, 7, 10, 15]
