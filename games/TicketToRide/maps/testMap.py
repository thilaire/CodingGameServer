# just to test the map

from csv import reader
from colorama import Fore, Back, Style
from itertools import zip_longest


def decomment(csvfile):
	"""removes the comments in a csv file
	(comments start with #)
	do not take into account if the comment is in a string or not (not necessary here)
	"""
	for row in csvfile:
		raw = row.split('#')[0].strip()
		if raw:
			yield raw

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

textColors = [
	('', Fore.RESET),
	('Purple', Style.BRIGHT + Fore.MAGENTA),            # PURPLE
	('White', Style.BRIGHT + Fore.LIGHTWHITE_EX),      # White
	('Blue', Fore.BLUE),                              # Blue
	('Yellow', Style.BRIGHT + Fore.LIGHTYELLOW_EX),             # Yellow
	('Orange', Style.BRIGHT + Fore.YELLOW),     # Orange
	('Black', Style.BRIGHT + Fore.BLACK),              # Black
	('Red', Style.BRIGHT + Fore.LIGHTRED_EX),        # Red
	('Green', Style.BRIGHT + Fore.GREEN),              # Green
	('Multi', Fore.WHITE)                       # Multi
]

textColors = [
	('', Fore.RESET),
	('Purple', Fore.MAGENTA),            # PURPLE
	('White',  Fore.LIGHTWHITE_EX),      # White
	('Blue', Fore.BLUE),                              # Blue
	('Yellow', Fore.LIGHTYELLOW_EX),             # Yellow
	('Orange', Fore.YELLOW),     # Orange
	('Black', Fore.BLACK),              # Black
	('Red', Fore.LIGHTRED_EX),        # Red
	('Green', Fore.GREEN),              # Green
	('Multi', Fore.WHITE)                       # Multi
]



BLOCK_S_NS = '\U00002502'     # '┃'
BLOCK_S_EW = '\U00002500'     # '━'
BLOCK_S_NE = '\U00002514'     # '┗'
BLOCK_S_NW = '\U00002518'     # '┛'
BLOCK_S_SE = '\U0000250C'     # '┏'
BLOCK_S_SW = '\U00002510'     # '┓'

BLOCK_D_NS = '\U00002551'     # '║'
BLOCK_D_EW = '\U00002550'     # '═'
BLOCK_D_NE = '\U0000255A'     # '╚'
BLOCK_D_NW = '\U0000255D'     # '╝'
BLOCK_D_SE = '\U00002554'     # '╔'
BLOCK_D_SW = '\U00002557'     # '╗'


dcol = {'N':  0, 'S': 0, 'E': 1, 'W': -1}
dlin = {'N': -1, 'S': 1, 'E': 0, 'W':  0}

BlockTr = {
	('N', ''): BLOCK_S_NS, ('S', ''): BLOCK_S_NS, ('E', ''): BLOCK_S_EW, ('W', ''): BLOCK_S_EW,
	('N', 'N'): BLOCK_S_NS, ('S', 'S'): BLOCK_S_NS, ('E', 'E'): BLOCK_S_EW, ('W', 'W'): BLOCK_S_EW,
	('N', 'E'): BLOCK_S_SE, ('N', 'W'): BLOCK_S_SW, ('S', 'E'): BLOCK_S_NE, ('S', 'W'): BLOCK_S_NW,
	('E', 'S'): BLOCK_S_SW, ('E', 'N'): BLOCK_S_NW, ('W', 'N'): BLOCK_S_NE, ('W', 'S'): BLOCK_S_SE
}

BlockWg = {
	('N', ''): BLOCK_D_NS, ('S', ''): BLOCK_D_NS, ('E', ''): BLOCK_D_EW, ('W', ''): BLOCK_D_EW,
	('N', 'N'): BLOCK_D_NS, ('S', 'S'): BLOCK_D_NS, ('E', 'E'): BLOCK_D_EW, ('W', 'W'): BLOCK_D_EW,
	('N', 'E'): BLOCK_D_SE, ('N', 'W'): BLOCK_D_SW, ('S', 'E'): BLOCK_D_NE, ('S', 'W'): BLOCK_D_NW,
	('E', 'S'): BLOCK_D_SW, ('E', 'N'): BLOCK_D_NW, ('W', 'N'): BLOCK_D_NE, ('W', 'S'): BLOCK_D_SE
}


BLOCK = '\U00002588'

mapFile = 'USA/map.txt'
citiesFile = 'USA/cities.csv'
tracksFile = 'USA/tracks.csv'


# build the list of cities
with open(citiesFile) as csvCities:
	cities = list(x for x in reader(decomment(csvCities), delimiter=';'))
	citiesName = [c[1] for c in cities]
	invCities = {c: i for i, c in enumerate(citiesName)}

# open the text map and store it in a 2D array (list of lists)
with open(mapFile) as txtMap:
	rawtxt = [list(line[:-1]) for line in txtMap]

# highlight the cities
for c in cities:
	lin, col, size = [int(t) for t in c[2:5]]
	for dc in range(size):
		rawtxt[lin-1][col + dc-1] = Back.LIGHTWHITE_EX + Fore.BLACK + rawtxt[lin-1][col + dc-1] + Fore.RESET + Back.RESET


# build the list of tracks
with open(tracksFile) as csvTracks:
	tracks = []
	for i, track in enumerate(reader(decomment(csvTracks), delimiter=';')):
		try:
			# draw the track
			co1 = textColors[colors[track[3]]][1]
			co2 = textColors[colors[track[4]]][1] if track[4] != "None" else co1
			lin = int(track[5])
			col = int(track[6])
			path = track[7]
			i = 0
			for cour, suiv in zip_longest(path, path[1:], fillvalue=''):
				co = co1 if i%2 else co2
				lin += dlin[cour]
				col += dcol[cour]
				ch = BlockTr[(cour, suiv)] if i != int(len(path) / 2) else track[2]
				if track[1] == 'New York' and track[0] == 'Montréal':
					co = Style.BRIGHT + co
					ch = BlockWg[(cour, suiv)] if i != int(len(path) / 2) else BLOCK
					ch = Fore.LIGHTRED_EX + Style.BRIGHT + ch
				else:
					co = Style.NORMAL + co
				rawtxt[lin-1][col-1] = co + ch + Fore.RESET + Style.NORMAL
				i += 1
		except IndexError:
			pass
		except ValueError:
			pass

#display both
with open(mapFile) as txtMap:
	for orig, modif in zip(txtMap, rawtxt):
		print(("%-60s" % orig[:-1]) + "".join(modif))
