"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire
Licence: GPL

File: Constants.py
	Contains the constants of the game Labyrinth
	-> defines the constants used for the client communication

Copyright 2021 T. Hilaire
"""

from colorama import Back, Fore

# constants defining a move
INSERT_LINE_LEFT = 0
INSERT_LINE_RIGHT = 1
INSERT_COLUMN_UP = 2
INSERT_COLUMN_DOWN = 3
OPPOSITE = {INSERT_LINE_LEFT: INSERT_LINE_RIGHT, INSERT_LINE_RIGHT: INSERT_LINE_LEFT,
			INSERT_COLUMN_UP: INSERT_COLUMN_DOWN, INSERT_COLUMN_DOWN: INSERT_COLUMN_UP}

MAX_ITEM = 24

TOPLEFT = {(True, True): "▛", (True, False): "▀", (False, True): "▌", (False, False): "▘"}
TOPMID = {True: "▀", False: "│"}
TOPRIGHT = {(True, True): "▜", (True, False): "▀", (False, True): "▐", (False, False): "▝"}
MIDLEFT = {True: "▌", False: "─"}
MIDMID = {(True, False, False, False): "┬", (False, True, False, False): "┤",
			(False, False, True, False): "┴", (False, False, False, True): "├",
			(True, True, False, False): "┐", (False, True, True, False): "┘",
			(False, False, True, True): "└", (True, False, False, True): "┌",
		}
MIDRIGHT = {True: "▐", False: "─"}
BOTTOMLEFT = {(True, True): "▙", (True, False): "▄", (False, True): "▌", (False, False): "▖"}
BOTTOMMID = {True: "▄", False: "│"}
BOTTOMRIGHT = {(True, True): "▟", (True, False): "▄", (False, True): "▐", (False, False): "▗"}

BACKPLAYER = {(True, True, False): Back.LIGHTMAGENTA_EX, (True, False, False): Back.LIGHTRED_EX, (False, True, False): Back.LIGHTBLUE_EX, (False, False, False): Back.RESET,
				(True, True, True): Back.LIGHTMAGENTA_EX, (True, False, True): Back.LIGHTRED_EX, (False, True, True): Back.LIGHTBLUE_EX, (False, False, True): Back.LIGHTGREEN_EX}
ITEMCHAR = {(True, True): Fore.MAGENTA, (True, False): Fore.MAGENTA, (False, True): Fore.BLUE, (False, False): ""}

LT_RANDOM = [True, True, True, False, False, False, False, False]