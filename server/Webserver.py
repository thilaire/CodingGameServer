"""
* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire, J. Brajard
Licence: GPL

File: webserver.py
	Contains the webserver routines (based on Flask)
	-> all the routes are defined here
	-> the template files used are in templates

Copyright 2016-2019 T. Hilaire, J. Brajard
"""

from flask import Flask, render_template, abort, send_from_directory, request, redirect
from jinja2 import ChoiceLoader, FileSystemLoader

from flask_socketio import SocketIO, send, emit, join_room
import threading
from os.path import isfile, join
from server.Game import Game
from server.Player import RegularPlayer
from server.Logger import Config
from server.Tournament import Tournament
from server.BaseClass import BaseClass

# flask object
flask = Flask("webserver")
socketio = SocketIO(flask)

# set the template paths so that in priority,
# it first looks in <gameName>/server/templates/ and then in CGS/server/templates
templatePaths = ['games/' + Game.getTheGameName() + '/server/templates/', 'server/templates/']


def runWebServer(host, port):
	"""
	Run the webserver
	"""
	# add a custom jinja loader
	my_loader = ChoiceLoader(
		[flask.jinja_loader, FileSystemLoader(templatePaths), ])
	flask.jinja_loader = my_loader

	# set some global variables
	flask.jinja_env.globals['base_url'] = '/'
	flask.jinja_env.globals['GameName'] = Game.getTheGameName()
	flask.jinja_env.globals['host'] = Config.host
	flask.jinja_env.globals['webPort'] = Config.webPort
	flask.jinja_env.globals['SubTitle'] = 'A CGS-based game'

	# Start the web server
	flask.logger.message('Run the web server on port %d...', port)
	flask.config['SECRET_KEY'] = 'QSDFGHJKLM|'

	socketio.run(flask, host=host, port=port, debug=True, use_reloader=False)


# # ================
# #   main page
# # ================
@flask.route('/')
@flask.route('/index.html')
def index():
	"""
	Main page (based on index.html template)
	"""
	return render_template('index.html')


# ================
#   static files
# ================
def static_file(fileName):
	"""
	Returns a static_file from the static paths
	The function first searches in the first path of the template path list (staticPaths).
	If the file exists, the function returns that file, otherwise it searches
	for the file in the next path...
	Redirects to error 404 if the file is not found.
	"""
	for path in templatePaths:
		if isfile(join(path, fileName)):
			return send_from_directory(path, fileName)
	abort(404)


# some static files
@flask.route('/favicon.ico')
def favicon():
	"""Returns the favicon"""
	return static_file('favicon.ico')


@flask.route('/style.css')
def css():
	"""Returns the CSS style"""
	return static_file('style.css')


@flask.route('/game/gamestyle.css')
def game_css():
	"""Returns the CSS game display style"""
	return static_file('game/gamestyle.css')


@flask.route('/banner.png')
def banner():
	"""Returns the pages top banner PNG file"""
	return static_file('banner.png')





# =======
#  Games
# =======
@flask.route('/new_game.html')
def new_game():
	"""
	Page to create a new game
	"""
	Players = '\n'.join(['<option>' + p.name + '</option>\n' for p in RegularPlayer.allInstances.values()])
	return render_template('game/new_game.html', list_players=Players)


@flask.route('/create_new_game.html', methods=['POST'])
def create_new_game():
	"""
	Receive the form to create a new game
	-> create the game (ie runPhase it)
	"""
	# get Players
	player1 = RegularPlayer.getFromName(request.form.get('player1'))
	player2 = RegularPlayer.getFromName(request.form.get('player2'))

	# !TODO: add some options (timeout, seed, etc.) in the html, and send them to the constructor
	try:
		# the constructor will check if player1 and player2 are available to play
		# no need to store the game object created here
		Game.getTheGameClass()(player1, player2)

	except ValueError as e:
		# !TODO: redirect to an error page
		# TODO: log this
		return 'Error. Impossible to create a game with ' + str(request.form.get('player1')) +\
			   ' and ' + str(request.form.get('player2')) + ': "' + str(e) + '"'
	else:
		redirect('/')


@flask.route('/game/<gameName>')
def game(gameName):
	"""Returns the webpage of a game
	<gameName> is the name of the game
	If the name is not valid, the answer with the noObject page
	"""
	g = Game.getFromName(gameName)

	if g:
		try:
			displayName = g.getCutename()
		except NotImplementedError:
			displayName = gameName
		return render_template('game/Game.html', host=Config.host, webPort=Config.webPort,
							   gameName=gameName, displayName=displayName, player1=g.players[0].HTMLrepr(),
							   player2=g.players[1].HTMLrepr())
	else:
		return render_template('noObject.html', className='game', objectName=gameName)


# ============
#  Tournament
# ============
@flask.route('/new_tournament.html')
def new_tournament():
	"""
	Page to create a new tournament
	Build from HTMLFormDict class method of TournamentMode (build from all the tournament modes)
	"""
	return render_template("tournament/new_tournament.html", **Tournament.HTMLFormDict(Game.getTheGameName()))


@flask.route('/create_new_tournament.html', methods=['POST'])
def create_new_tournament():
	"""
	Receive the form to create a new tournament
	"""
	# create the tournament
	try:
		Tournament.factory(**dict(request.form))
	except ValueError as e:
		# !TODO: redirect to an error page
		# TODO: log this
		return 'Error. Impossible to create a tournament with ' + str(dict(request.form)) + ':"' + str(e) + '"'
	else:
		redirect('/')


@flask.route('/tournament/<tournamentName>')
def tournament(tournamentName):
	"""
	Web page for a tournament
	redirect to `noTournament.html` if tournament doesn't exist
	Parameters:
	- tournamentName: name of the tournament
	"""
	t = Tournament.getFromName(tournamentName)
	if t:
		return render_template('tournament/tournament.html', t=t, host=Config.host, webPort=Config.webPort)
	else:
		return render_template('noObject.html', className='tournament', objectName=tournamentName)



@flask.route('/run_tournament/<tournamentName>', methods=['POST'])
def runTournament(tournamentName):
	"""
	Receive the runPhase tournament form
	redirect to `noTournament.html` if the tournament doesn't exit
	other, return nothing, since it is run from ajax (doesn't wait for any response)
	Parameters:
	- tournamentName: name of the tournament
	"""
	t = Tournament.getFromName(tournamentName)
	if t:
		threading.Thread(target=t.runPhase, kwargs=dict(request.form)).start()
	else:
		return render_template('noObject.html', className='tournament', objectName=tournamentName)


# =========
#  Player
# =========

@flask.route('/player/<playerName>')
def player(playerName):
	"""
	Web page for a player
	Redirects to `noPlayer.html` if the player doesn't exist
	"""
	pl = RegularPlayer.getFromName(playerName)
	if pl:
		# TODO: use a template
		return render_template('player/Player.html', host=Config.host, webPort=Config.webPort, playerName=playerName)
	else:
		return render_template('noObject.html', className='player', objectName=playerName)



@flask.route('/player/disconnect/<playerName>')
def disconnectPlayer(playerName):
	"""
	Disconnect a player
	Only for debug...
	:param playerName:
	:return:
	"""
	# !FIXME: activate this only in debug or dev mode
	# TODO: if necessary, add a disconnectAllPlayer
	pl = RegularPlayer.getFromName(playerName)
	if pl:
		pl.disconnect()
		redirect('/')
	else:
		return render_template('noObject.html', className='player', objectName=playerName)


# ==========
# Websockets
# ==========
# TODO: can be directly obtained from {x.__name__:x for x in WebSocket.__subclasses__()}
wsCls = {'Games': Game, 'Players': RegularPlayer, 'Tournaments': Tournament}


@socketio.on('join')
def websocket_class(data):
	print('Join',data)
	join_room(data)
	Game.sendListofInstances()



# @flask.route('/websocket/ListOfInstances')
# def classWebSocket():
# 	"""
# 	Websocket for the list of instances of the classes Game, Player and Tournament
# 	-> used to get the a json with the list of instances of theses classes
# 	"""
# 	# should be a websocket
# 	wsock = request.environ.get('wsgi.websocket')
# 	if not wsock:
# 		abort(400, 'Expected Websocket request.')
# 	# register this websocket
# 	BaseClass.registerLoIWebSocket(wsock)
# 	# send to this websocket
# 	BaseClass.sendListofInstances(wsock)
# 	# loop until the end of this websocket
# 	while True:
# 		try:
# 			wsock.receive()
# 		except WebSocketError:
# 			BaseClass.removeLoIWebSocket(wsock)
# 			break







#
# @route('/websocket/<clsName>/<name>')
# def classWebSocket(clsName, name):
# 	"""
# 	Websocket for an instance of the classes Game, Player or Tournament
# 	-> used to get the a json with informations about this object
#
# 	"""
# 	# should be a websocket
# 	wsock = request.environ.get('wsgi.websocket')
# 	if not wsock:
# 		abort(400, 'Expected Websocket request.')
# 	# check if that instance exists
# 	if clsName not in wsCls:
# 		abort(400, 'Invalid class %s is not in %s' % (clsName, wsCls.keys()))
# 	cls = wsCls[clsName]
# 	obj = cls.getFromName(name)
# 	if obj is None:
# 		abort(400, 'Invalid name (%s) for class %s' % (name, clsName))
# 	# register this websocket
# 	obj.registerWebSocket(wsock)
# 	# send to this websocket
# 	obj.sendUpdateToWebSocket(wsock)
# 	# loop until the end of this websocket
# 	while True:
# 		try:
# 			wsock.receive()
# 		except WebSocketError:
# 			BaseClass.removeLoIWebSocket(wsock)
# 			break
#
#


# ======
#  logs
# =======
# @flask.route('logs/')
# def log():
# 	"""Returns the log.html"""
# 	return


@flask.route('/logs/activity')
def activity():
	"""Returns the activity.log file"""
	return send_from_directory(Config.logPath, 'activity.log')

@flask.route('/logs/errors')
def log():
	"""Returns the errors.log file"""
	return send_from_directory(Config.logPath, 'errors.log')


@flask.route('/logs/player/<playerName>')
def logP(playerName):
	"""
	Returns a player log file
	:param playerName: (string) name of the player
	"""
	return send_from_directory(join(Config.logPath, 'Players'), playerName+'.log')


@flask.route('/logs/game/<gameName>')
def logG(gameName):
	"""
	Returns a game log file
	:param gameName: (string) name of the game
	"""
	return send_from_directory(join(Config.logPath, 'Games'), gameName + '.log')


@flask.route('/logs/tournament/<tournamentName>')
def logT(tournamentName):
	"""
	Returns a tournament log file
	:param tournamentName: (string) name of the game
	"""
	return send_from_directory(join(Config.logPath, 'Tournaments'), tournamentName + '.log')


# ================
#   info page
# ================
@flask.route('/about.html')
def about():
	"""
	About page
	"""
	return render_template("about.html")


# =======
#  errors
# ========
@flask.errorhandler(404)
def error404(err):
	"""Returns error 404 page"""
	# TODO: log this
	return render_template('error404.html', message=err)


@flask.errorhandler(500)
def errror500(err):
	"""
	Return for error 500
	"""
	# TODO: return a full page ?
	flask.logger.error(err, exc_info=True)
	return "We have an unexpected error. It has been reported and logged,"\
		   " and we will work on it so that it never occurs again !"



