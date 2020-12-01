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

from _collections import OrderedDict
from colorama import Fore, Back, Style

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
	('', Fore.RESET),
	('Purple', Style.BRIGHT + Fore.MAGENTA),            # PURPLE
	('White', Style.BRIGHT + Fore.LIGHTWHITE_EX),      # White
	('Blue', Fore.BLUE),                              # Blue
	('Yellow', Style.BRIGHT + Fore.YELLOW),             # Yellow
	('Orange', Style.BRIGHT + Fore.LIGHTYELLOW_EX),     # Orange
	('Black', Style.BRIGHT + Fore.BLACK),              # Black
	('Red', Style.BRIGHT + Fore.LIGHTRED_EX),        # Red
	('Green', Style.BRIGHT + Fore.GREEN),              # Green
	('Multi', Fore.LIGHTBLUE_EX)                       # Multi
]


# score for the tracks
Scores = [0, 1, 2, 4, 7, 10, 15]
