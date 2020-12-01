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


BLOCK_NS = '\U00002503'     # '┃'
BLOCK_EW = '\U00002501'     # '━'
BLOCK_NE = '\U00002517'     # '┗'
BLOCK_NW = '\U0000251B'     # '┛'
BLOCK_SE = '\U0000250F'     # '┏'
BLOCK_SW = '\U00002513'     # '┓'

dcol = {'N':  0, 'S': 0, 'E': 1, 'W': -1}
dlin = {'N': -1, 'S': 1, 'E': 0, 'W':  0}

Block = {
	('N', ''): BLOCK_NS, ('S', ''): BLOCK_NS, ('E', ''): BLOCK_EW, ('W', ''): BLOCK_EW,
	('N', 'N'): BLOCK_NS, ('S', 'S'): BLOCK_NS, ('E', 'E'): BLOCK_EW, ('W', 'W'): BLOCK_EW,
	('N', 'E'): BLOCK_SE, ('N', 'W'): BLOCK_SW, ('S', 'E'): BLOCK_NE, ('S', 'W'): BLOCK_NW,
	('E', 'S'): BLOCK_SW, ('E', 'N'): BLOCK_NW, ('W', 'N'): BLOCK_NE, ('W', 'S'): BLOCK_SE
}


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
		rawtxt[lin-1][col + dc-1] = Fore.LIGHTWHITE_EX + Back.BLACK + rawtxt[lin-1][col + dc-1] + Fore.RESET + Back.RESET


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
				rawtxt[lin-1][col-1] = co + Block[(cour, suiv)] + Fore.RESET
				i += 1
		except IndexError:
			pass
		except ValueError:
			pass

#display both
with open(mapFile) as txtMap:
	for orig, modif in zip(txtMap, rawtxt):
		print(("%-60s" % orig[:-1]) + "".join(modif))
