"""
* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: B. Lamon, based on T. Hilaire & J. Brajard's template file.
Licence: GPL

File: SDGameHandler.py
	Contains the class SDGameHandler
	->	Defines all the elements needed for the game + checks to make sure every move is legal.

Copyright 2025 B. Lamon
"""

from .Constants import *
from typing import Tuple, List

class SDGameHandler:
    def __init__(self):
        # BOARD COMPLETION MAP - will be useful?
        # Says where to put the next token
        # to cast into n-tuples?
        self.boardCompletion = (
            ("E", "E", "E", "E", "S"),	# North
            ("N", "E", "E", "S", "S"),	# South
            ("N", "N", "S", "S", "S"),	# East
            ("N", "N", "W", "S", "S"),	# West
            ("N", "W", "W", "W", None)	# None when complete (index (4,4)), beginning at index (2,2)
        )

        self._board = [
            [None, None, None, None, None],  # 5*5 matrix. Each member of the matrix represents a case of the board.
            [None, None, None, None, None],  # On each case of the board, there will be a token distributed (1st turn),
            [None, None, None, None, None],  # then a little less etc. depending on player decisions each move.
            [None, None, None, None, None],  # TODO: Requires getter + setter ?
            [None, None, None, None, None]
        ]                   # TODO! How do we represent each token on the matrix?

        # Memo

        #NONE = None
        #PEARL = 1
        #GOLD = 2
        #BLUE_SAPPHIRE = 3
        #DIAMOND = 4
        #EMERALD = 5
        #RUBY = 6
        #OBSIDIAN = 7
        self.tokens = [0,0,0,0,0,0,0,0]

        #same as Memo ? + privilege + crown. What else?
        #OR, we may represent inventories this way:
        # [None, [Jewel cards , Tokens], [Jewel cards , Tokens], ... , [Jewel cards , Tokens], Priv_Scrolls, crowns]
        #   (None is used to sync the indices)
        #   Anything else needed?
        self.inventoryP1 = [None, [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], 0, 0]
        self.inventoryP2 = [None, [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], 0, 0]





    # getter for the board
    @property
    def board(self):
        return self._board

    # setter for the board
    def update_board(self, value: int, position: Tuple[int,int]):
        x,y = position
        self._board[x][y] = value

    def nextPosition(self, currentPosition: List[int]):
        """
        returns the position of the next element to check?
        Memo: x is the row, y the column...
        """
        x,y = currentPosition

        if self.boardCompletion[x][y] == "N":
            nextPosition = [x - 1, y]
        elif self.boardCompletion[x][y] == "S":
            nextPosition = [x + 1, y]
        elif self.boardCompletion[x][y] == "E":
            nextPosition = [x, y + 1]
        elif self.boardCompletion[x][y] == "W":
            nextPosition = [x, y - 1]
        else:
            nextPosition = [-1,-1]
        return nextPosition



    # all the tokens are here
    #TODO
    def bank(self):
        """
        Defines the bank aka where all the tokens to distribute belong.
        So we'll use this method whenever a player chooses to redistribute the tokens on the board
        (+ the privilege, but it's not handled here)

            -> returns a list with all available tokens (will be used to redistribute)
        """
        countedTokens = [None,0,0,0,0,0,0,0]
        #TODO: run through all the board, count every token into a list
        #first position index: (2,2)
        #then we run following the board?
        #maybe implement a method which gives the next position?
        # -> done
        # N.B. can't use "if x == None:", should use "if x is None:"

        #while the next is != None,

        # run through all the board, starting at the center
        coords = [2,2]
        # While the position is within the board
        while coords != [-1,-1]:
            #go to the board, add the current thing to the list
            x, y = coords
            match self.board[x][y]:
                case None:
                    #go to the next position on the board
                    pass
                case 1:
                    countedTokens[PEARL] += 1
                case 2:
                    countedTokens[GOLD] += 1
                case 3:
                    countedTokens[BLUE_SAPPHIRE] += 1
                case 4:
                    countedTokens[DIAMOND] += 1
                case 5:
                    countedTokens[EMERALD] += 1
                case 6:
                    countedTokens[RUBY] += 1
                case 7:
                    countedTokens[OBSIDIAN] += 1
                case _:
                    #TODO: raise an error?
                    print("ERROR: couldn't count a token on the board (Not a token nor \"None\")")
            coords = self.nextPosition(coords)
        #out of the while cdt





        # NEVER MIND THAT'S NOT HOW YOU COUNT THE TOKENS TO REDISTRIBUTE
        # We need to count the token each player has + the tokens on the board. That gives us the tokens we can NOT
        # redistribute. Then we just subtract those to the max amount and voilà, we have the amount of available tokens.

        #TODO: Run through the inventories of the two players, count every token into the list previously incremented

        bank = [None, 2, 3, 4, 4, 4, 4, 4]

        #Checking if there's too many token, which shouldn't happen
        # TODO: how to handle an error?
        #  should I create a class that inherits from ValueError then raises it, or should I just raise a ValueError?

        # Max amount of pearls = 2
        if countedTokens[1] > 2:
            print(f"ERROR: counted too many {tokenTypes[1]} tokens!")  # tokenTypes: see Constants.py
        # Max amount of gold = 3
        if countedTokens[2] > 3:
            print(f"ERROR: counted too many {tokenTypes[2]} tokens!")  # tokenTypes: see Constants.py

        for i in range(1,len(countedTokens)):
            #we already did the first two cases, so we pass them
            if i > 2:
                #the rest of the tokens aren't supposed to exceed 4
                if countedTokens[i] > 4:
                    print(f"ERROR: counted too many {tokenTypes[i]} tokens!") # tokenTypes: see Constants.py

            bank[i] -= countedTokens[i]
        return bank




    def redistribute(self):
        toShuffle = self.bank()

        #TODO: shuffle the tokens and redistribute them alongside what's already on the board
        #Basically, we go on the board, we check if the first index. If it's already full, we go to the next (case given
        #by the self._boardCompletion map).
        #If a case is empty, we randomly choose one of the indices from the list of the bank. If the index is empty,
        #we go to the next (then the next and whatnot) until we get to an available token.
        #If there's not available token, the distribution is done
        # TODO: how do we detect that?
