"""

* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: T. Hilaire, T. Gautier
Licence: GPL

File: clientAPI.py
	A python version of the clientAPI

Copyright 2019 T. Hilaire, T. Gautier
"""

import socket
import sys
from logging import getLogger

# some constants
NORMAL_MOVE = 0
WINNING_MOVE = 1
LOOSING_MOVE = -1


class ClientAPI:
	"""Simple API for the client
	Served as a based class to be extended"""
	def __init__(self, serverName, port, name):
		"""Initialize the game
		debug is the debug level"""
		self._servername = serverName
		self._port = port
		self.playerName = name
		# logger
		self._logger = getLogger('CGS')


	def dispError(self, fct, msg):
		"""Display error"""
		# TODO: should be done with logger package
		print("\033[5m\033[31m\u2327\033[2m [%s] (%s)\033[0m %s" % (self.playerName, fct, msg))
		sys.exit(1)
	
	def dispDebug(self, fct, level, msg):
		"""Display debug"""
		# TODO: should be done with logger package
		if self.debug >= level:
			print("\033[35m\u26A0\033[0m [%s] (%s) %s" % (self.playerName, fct, msg), file=sys.stderr)

	def sendString(self, fct, msg):
		"""Send string through socket and acknowledge"""
		self.sock.send(msg.encode())
		self.dispDebug(fct, 2, "Send '%s' to the server" % msg)

		res = self.read_inbuf(fct)

		if res != "OK":
			self.dispError(fct, "Error: The server does not acknowledge, but answered:\n%s" % res)
		self.dispDebug(fct, 3, "Receive acknowledgment from the server")

	def read_inbuf(self, fct):
		"""Read data through socket"""
		length = int(self.sock.recv(4).decode())

		self.dispDebug(fct, 3, "prepare to receive a message of length :%lu" % length)

		buffer = ""
		read_length = 0
		while read_length < length:
			res = self.sock.recv(length - read_length)
			read_length += len(res)
			buffer += res.decode()
				
		return buffer

	def __enter__(self):
		self.dispDebug("", 2, "Initiate connection with %s (port: %d)" % (self._serverName, self._port))

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self._serverName, self._port))

		self.sendString("", "CLIENT_NAME %s" % self.name)
	
	def __exit__(self):
		self.sock.close()

	def waitForGame(self, fct, training = ""):
		if training != "":
			self.sendString(fct, "WAIT_GAME %s" % training)
		else:
			self.sendString(fct, "WAIT_GAME ")
		
		gameName = "NOT_READY"
		while gameName == "NOT_READY":
			gameName = self.read_inbuf(fct)
		
		self.dispDebug(fct, 1, "Receive Game name=%s" % gameName)

		# read game size
		buffer = self.read_inbuf(fct)

		self.dispDebug(fct, 2, "Receive Game sizes=%s" % buffer)

		return gameName, buffer
	
	def getGameData(self, fct):
		self.sendString(fct, "GET_GAME_DATA")

		# read game data
		data = self.read_inbuf(fct)

		self.dispDebug(fct, 2, "Receive game's data:%s" % data)

		# read if we begin (0) or if the opponent begins (1)
		buffer = self.read_inbuf(fct)

		self.dispDebug(fct, 2, "Receive these player who begins=%s" % buffer)
		
		return (data, int(buffer)) 
	
	def getCGSMove(self, fct):
		self.sendString(fct, "GET_MOVE")

		# read move
		move = self.read_inbuf(fct)
		self.dispDebug(fct, 1, "Receive that move:%s" % move)

		# read the return code
		buffer = self.read_inbuf(fct)
		self.dispDebug(fct, 2, "Receive that return code:%s" % buffer)

		# extract result
		result = int(buffer)
		self.dispDebug(fct, 2,"results=%d" % result)
		return (move, result)

	def sendCGSMove(self, fct, move):
		self.sendString(fct, "PLAY_MOVE %s" % move)

		# read return code
		buffer = self.read_inbuf(fct)
		self.dispDebug(fct, 2, "Receive that return code:%s" % buffer)

		result = int(buffer)
		self.dispDebug(fct, 2,"results=%d" % result)

		# read msg
		buffer = self.read_inbuf(fct)
		self.dispDebug(fct, 1,"Receive that message: %s" % buffer)

		return result

	def printGame(self, fct):
		self.dispDebug(fct, 2, "Try to get string to display Game")

		self.sendString(fct, "DISP_GAME")

		buffer = self.read_inbuf(fct)
		print(buffer)
	
	def sendCGSComment(self, fct, comment):
		self.dispDebug(fct, 2, "Try to send a comment")

		if len(comment) > 100:
			self.dispError(fct, "The Comment is more than 100 characters.")
		self.sendString(fct, "SEND_COMMENT %s" % comment)
		