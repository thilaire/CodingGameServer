from clientAPI import ClientAPI

class SnakeAPI(ClientAPI):
	def connectToServer(self, serverName, port, name):
		self.connectToCGS(self.connectToServer.__name__, serverName, port, name)
	
	def closeConnection(self):
		self.closeCGSConnection(self.closeConnection.__name__)
	
	def waitForSnakeGame(self, gameType):
		gameName, data = self.waitForGame(self.waitForSnakeGame.__name__, gameType)

		tab = data.split(" ")

		return (gameName, tab[0], tab[1], tab[2])
	
	def getSnakeArena(self):
		data, player = self.getGameData(self.getSnakeArena.__name__)

		walls_str = data.split()

		walls = [int(wall) for wall in walls_str]

		return (walls, player)
	
	def getMove(self):
		move, ret = self.getCGSMove(self.getMove.__name__)

		move = int(move)

		self.dispDebug(self.getMove.__name__, 2, "move: %d, ret: %d" % (move, ret))
		return (move, ret)
	
	def sendMove(self, move):
		move = str(move)
		self.dispDebug(self.sendMove.__name__, 2, "move send : %s" % (move))
		return self.sendCGSMove(self.sendMove.__name__, move)

	def printArena(self):
		self.printGame(self.printArena.__name__)
	
	def sendComment(self, comment):
		self.sendComment(self.sendComment.__name__, comment)