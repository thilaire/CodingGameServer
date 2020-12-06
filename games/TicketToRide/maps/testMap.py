# just to test the map

from csv import reader
from colorama import Fore, Back
from random import choice

from games.TicketToRide.server.Track import Track
from games.TicketToRide.server.Constants import colorNames


def decomment(csvfile):
	"""removes the comments in a csv file
	(comments start with #)
	do not take into account if the comment is in a string or not (not necessary here)
	"""
	for row in csvfile:
		raw = row.split('#')[0].strip()
		if raw:
			yield raw


map = 'small'
mapFile = map+'/map.txt'
citiesFile = map+'/cities.csv'
tracksFile = map+'/tracks.csv'


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
			# build the track and draw it
			cities = (invCities[track[0]], invCities[track[1]])
			length = int(track[2])
			col = (colorNames.index(track[3]), colorNames.index(track[4]))
			pos = (int(track[5]), int(track[6]))
			path = track[7]
			# build the track, and plot it (in rawtxt)
			tr = Track(cities, length, col, pos, path)
			tr._taken = True    # choice([False]*10+[True])
			tr._player = choice([0,1])
			tr.draw(rawtxt)
		except IndexError:
			pass
		except ValueError:
			pass

#display both
with open(mapFile) as txtMap:
	for orig, modif in zip(txtMap, rawtxt):
		print(("%-60s" % orig[:-1]) + "".join(modif))
