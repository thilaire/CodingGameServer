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

class ClientAPI:
	def __init__(self, debug = 1):
		self.playerName = ""
		self.debug = debug

	def dispError(self, fct, msg):
		print("\033[5m\033[31m\u2327\033[2m [%s] (%s)\033[0m %s" % (self.playerName, fct, msg))
		sys.exit(1)
	
	def dispDebug(self, fct, level, msg):
		if self.debug >= level:
			print("\033[35m\u26A0\033[0m [%s] (%s) %s" % (self.playerName, fct, msg), file = sys.stderr)

	def sendString(self, fct, msg):
		self.sock.send(msg.encode())
		self.dispDebug(fct, 2, "Send '%s' to the server" % msg)

		res = self.read_inbuf(fct)

		if res != "OK":
			self.dispError(fct, "Error: The server does not acknowledge, but answered:\n%s" % res)
		self.dispDebug(fct, 3, "Receive acknowledgment from the server")

	def read_inbuf(self, fct):
		length = int(self.sock.recv(4).decode())

		self.dispDebug(fct, 3, "prepare to receive a message of length :%lu" % length)

		buffer = b""
		read_length = 0
		while read_length < length:
			res = self.sock.recv(length - read_length)
			read_length += len(res)
			buffer += res
				
		return buffer.decode()

	def connectToCGS(self, fct, serverName, port, name):
		self.playerName = name

		self.dispDebug(fct, 2, "Initiate connection with %s (port: %d)" % (serverName, port))

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((serverName, port))

		self.sendString(fct, "CLIENT_NAME %s" % name)
	
	def closeCGSConnection(self, fct):
		self.sock.close()

	def waitForGame(self, fct, training = ""):
		if training != "":
			self.sendString(fct,"WAIT_GAME %s" % training)
		else:
			self.sendString(fct, "WAIT_GAME ")
		
		gameName = "NOT_READY"
		while gameName == "NOT_READY":
			gameName = self.read_inbuf(fct)
		
		self.dispDebug(fct, 1, "Receive Game name=%s" % gameName)

		# read Labyrinth size
		buffer = self.read_inbuf(fct)

		self.dispDebug(fct, 2, "Receive Game sizes=%s" % buffer)

		return (gameName, buffer)
	
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
		