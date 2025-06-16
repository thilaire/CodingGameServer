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
from typing import Tuple, List, Iterator
from random import randint, seed

seed(1)

class SDGameHandler:
    def __init__(self):
        # BOARD COMPLETION MAP - will be useful
        # Says where to put the next token
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
            [None, None, None, None, None],
            [None, None, None, None, None]
        ]

        # Memo
        #
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
        self.temp = [0,0]


    # getter for the board
    @property
    def board(self):
        return self._board


    # setter for the board
    def update_board(self, value: None|int, position: Tuple[int]|List[int]):
        x,y = position
        self._board[x][y] = value


    def nextPosition(self, currentPosition: List[int]) -> List[int]:
        """
        returns the position of the next element to check?
        Memo:   - currentPosition = [x,y];
                - x is the row, y the column.
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
        elif self.boardCompletion[x][y] is None:
            nextPosition = [-1,-1]
        else:
            print("ERROR: no location on the board completion map!")
        return nextPosition


    def bank(self) -> List[int|None]:
        """
        Defines the bank aka where all the tokens to distribute belong.
        So we'll use this method whenever a player chooses to redistribute the tokens on the board
        (+ the privilege, but it's not handled here)

            -> returns a list with all available tokens (will be used to redistribute)
        """
        # all the tokens are here in the beginning, caus nobody has any, nor does the board
        bank = [None, 2, 3, 4, 4, 4, 4, 4]
        countedTokens = [None, 0, 0, 0, 0, 0, 0, 0]
        #first position index: (2,2)
        #then we run following the board by using nextPosition((x,y))

        # run through all the board, starting at the center
        coords = [2,2]
        # While the position isn't outside the board
        while coords != [-1,-1]:
            #go to the board, add the current thing to the list
            x, y = coords
            if self.board[x][y] is not None:
                countedTokens[self.board[x][y]] += 1
            coords = self.nextPosition(coords)

        # We need to count the token each player has + the tokens on the board. That gives us the unavailable tokens.
        # Then we just subtract those to the max amount and voilà, we have the amount of tokens in the bank.

        #self.inventoryP1 = [None, [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], 0, 0]
        # [jewel_card , token]
        for gemstone in range(1,8):
            countedTokens[gemstone] += self.inventoryP1[gemstone][1]
            countedTokens[gemstone] += self.inventoryP2[gemstone][1]

        #Checking if there's too many tokens, which shouldn't happen

        # Max amount of pearls = 2
        if countedTokens[PEARL] > 2:
            print(f"ERROR: counted too many {tokenTypes[PEARL]} tokens!")  # tokenTypes: see Constants.py
        # Max amount of gold = 3
        if countedTokens[GOLD] > 3:
            print(f"ERROR: counted too many {tokenTypes[PEARL]} tokens!")  # tokenTypes: see Constants.py

        for gemstone in range(1,len(countedTokens)):
            #we already did the first two cases, so we pass them
            if gemstone > 2:
                #the rest of the tokens aren't supposed to exceed 4
                if countedTokens[gemstone] > 4:
                    print(f"ERROR: counted too many {tokenTypes[gemstone]} tokens!") # tokenTypes: see Constants.py
            bank[gemstone] -= countedTokens[gemstone]

        return bank


    def addToInventory(self, player: int, _type: int, amount: int = 0, isToken: int = 1) -> None:
        """
        Adds an item in a player's inventory, with a specified amount

        By default, if we want a player to have one diamond, it'll be a token, unless 0 is specified as isToken,
        which case it is certain the player bought a jewel card of the type (unless I forgot a rule that specifies otherwise).
        """
        # Jewel Card
        # Token
        # Crown
        # TODO I guess
        #   !! when reaching 3 or 6 crowns
        #   call a new method, "chooseCrownCard()" or smth
        # Privilege Scrolls

        # I believe this creates copies of the inventories instead of pointers/references...
        # I do now know how to manage them so if I figure out how to create one, I'll do so because it looks cleaner
        selectedPlayer = list()
        if player == 1:
            selectedPlayer = self.inventoryP1
        elif player == 2:
            selectedPlayer = self.inventoryP2
        else:
            print("ERROR: unrecognised player (should be 1 or 2)")

        #add stuff to the inventory (we'll check afterwards)
        match _type:
            case 1: # PEARL
                if isToken:
                    # We add the requested amount...
                    selectedPlayer[1][1] += amount
                    # ...then we check whether the values are in the good range (max/min token amount).
                    # And we inform when there's an issue.
                    if selectedPlayer[1][1] > 2 or selectedPlayer[1][1] <= -2:
                        # Plural
                        print(
                            f"ERROR: Player {player} has {selectedPlayer[1][1]} pearl tokens!")  # Plural if x ∈ ℝ\{(-2;2)}...
                    elif selectedPlayer[1][1] < 0:
                        print(f"ERROR: Player {player} has {selectedPlayer[1][1]} pearl token!")  # ...otherwise, singular
                        # (from what I know).
                else:
                    print("ERROR: no pearl jewel card exist in the game!")

            case 2: # GOLD
                if isToken:
                    selectedPlayer[2][1] += amount
                    if selectedPlayer[2][1] > 3 or selectedPlayer[2][1] <= -2:
                        print(f"ERROR: Player {player} has {selectedPlayer[2][1]} gold tokens!")
                    elif selectedPlayer[2][1] < 0:
                        print(f"ERROR: Player {player} has {selectedPlayer[2][1]} gold token!")
                else:
                    print("ERROR: no gold jewel card exist in the game!")

            case 8: # PRIVILEGES
                selectedPlayer[8] += amount
                print(selectedPlayer)

            case 9: # CROWNS
                selectedPlayer[9] += amount

            case _:
                if 8 > _type > 2: # GEMSTONES
                    if isToken:
                        selectedPlayer[_type][1] += amount
                    else:
                        selectedPlayer[_type][0] += amount

                else:
                    print("ERROR: not a token nor a valid object (should be unreachable)!")


        # checking whether it's a legal move or not
        for i in range(1,10):
            if i < 8: # gemstones+pearls+golds
                #check whether they have enough jewellery card in a single gemstone
                if selectedPlayer[i][0] >= 10:
                    print(f"Player {player} has {selectedPlayer[i][0]} jewel cards of {tokenTypes[i]} and won the game! Congratulations :)")
                #negative amount of a gemstone jewel card
                if selectedPlayer[i][0] <= -2:
                    print(f"ERROR: {player} has {selectedPlayer[i][0]} jewel cards of {tokenTypes[i]}!")  # plural
                elif selectedPlayer[i][0] < 0:
                    print(f"ERROR: {player} has {selectedPlayer[i][0]} jewel card of {tokenTypes[i]}!") #singular

                #incorrect amount of tokens
                if selectedPlayer[i][1] > 4 or selectedPlayer[i][1] <= -2:
                    print(f"ERROR: Player {player} has {selectedPlayer[i][1]} {tokenTypes[i]} tokens!") # Plural if x ∈ ℝ\{(-2;2)}...
                elif selectedPlayer[i][1] < 0:
                    print(f"ERROR: Player {player} has {selectedPlayer[i][1]} {tokenTypes[i]} token!")  # ...otherwise, singular

            #privilege checks
            if i == 8:
                if selectedPlayer[8] > 3:
                    print(f"ERROR: Player {player} has {selectedPlayer[8]} privileges!")
                elif selectedPlayer[8] <= -2:
                    print(f"ERROR: Player {player} has {selectedPlayer[8]} privileges!")    # Plural if x ∈ ℝ\{(-2;2)}...
                elif selectedPlayer[8] < 0:
                    print(f"ERROR: Player {player} has {selectedPlayer[8]} privilege!")     # ...otherwise, singular
                                                                                            # (from what I know).
            #crown checks
            if i == 9:
                if selectedPlayer[9] >= 10:
                    print(f"Player {player} has {selectedPlayer[9]} crowns and won the game! Congratulations :)")
                elif selectedPlayer[9] <= -2:
                    print(f"ERROR: Player {player} has {selectedPlayer[8]} crowns!")    # Plural if x ∈ ℝ\{(-2;2)}...
                elif selectedPlayer[9] < 0:
                    print(f"ERROR: Player {player} has {selectedPlayer[8]} crown!")     # ...otherwise, singular
                                                                                        # (even though we're working w/ ints)
                elif selectedPlayer[9] == 3 or selectedPlayer[9] == 6:
                    #TODO
                    # should probably implement something to know whether they've already chosen a crown card
                    self.pickCrownCard(player)

        if player == 1:
            self.inventoryP1 = selectedPlayer
            #print(selectedPlayer)
        elif player == 2:
            self.inventoryP2 = selectedPlayer
            #print(selectedPlayer)
        else:
            print("ERROR: unrecognised player (should be 1 or 2)")

    def pickCrownCard(self, player):
        #copy of player inventory
        selectedPlayer = list()
        if player == 1:
            selectedPlayer = self.inventoryP1
        elif player == 2:
            selectedPlayer = self.inventoryP2
        else:
            print("ERROR: unrecognised player (should be 1 or 2)")

        if selectedPlayer[8] == 3 or selectedPlayer[8] == 6:
            #temp represents whether they've chosen a card or not
            if self.temp[player-1] == 0:
                print(f"Player {player} shall pick a crown card {Fore.GREEN} (TODO){Fore.RESET}.")
            elif self.temp[player-1] == 1:
                print(f"ERROR: Player {player} should've picked a crown card {Fore.RED} (TODO){Fore.RESET}.")
        else:
            print(f"ERROR: Player {player} shouldn't have chosen a crown card!")
        self.temp[player-1] = 1


    def redistribute(self) -> None:

        #Basically, we go on the board, we check the first index. If it's already full, we go to the next (case given
        #by the self._boardCompletion map).
        #If a case is empty, we randomly choose one of the indices from the list of the bank. If the index is empty,
        #we choose another one until we get to an available token.
        #If there's no available token, the distribution is done

        # algorithm idea:
        # while the next case isn't -1-1,
        #   if the case isn't complete
        #       take a random token from the bank,
        #       put it on the board
        #       subtract it to the bank
        #   go to the next case

        coords = [2,2]
        bank = self.bank()

        # browse the board
        for position in PositionIterator(coords):
            x, y = position

            if self.board[x][y] is None:
                #random token from the bank
                #Can most likely be optimised.
                #e.g. pop the random one which doesn't work from the [1,2,...,7] list, then choose from it?
                randomToken = randint(1,7)  # TODO: implement the seed for random generation!!!

                #wait until we're in a case which is not full
                while bank[randomToken] == 0:
                    randomToken = randint(1,7)

                self.update_board(randomToken, (x,y))
                bank[randomToken] -= 1

        #need to check whether the bank is empty?
        for token in range(1,7):
            if bank[token] != 0:
                print(f"ERROR: the bank isn't empty after refilling the board! (item {tokenTypes[token]}: {bank[token]} in the bank)")



        #TODO: privilege scroll management (memo: redistribute, 3-token capture, take from opponent, use one)
        # TODO: choose tokens on the board
        # TODO
        #   Substitution of any token for a gold one (when buying a card for instance)
        #   idea: count every token required for a card. If there isn't enough, count gold tokens, and add them to those
        #   uncompleted. If there's still not enough, then it's illegal.

    def tokenCapture(self,coords: list[list], playerInventory) -> None:
        """
        checks whether the list of coordinates given is legit. (<4 elements in the list, all following each other in vertical,
        horizontal or diagonal).
        Then we check whether there's a gold token, which case the move is illegal.
        Then we check whether the three tokens are identical, or whether there's two pearls chosen, which case the
        opponent gets a privilege scroll.
        """

        if len(coords) > 3:
            print("ERROR: You can only capture 3 tokens at most!")
            return
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        x3, y3 = coords[2]
        #checking whether the second case is next to the first
        firstCheck = [x1-x2, y1-y2]

        # We should check whether a move is legal (inline + within board + no gold and whatnot)

        directionsList = [
            [1,1], #TOP LEFT
            [0,1], #STRAIGHT LEFT
            [-1,1],#BOTTOM LEFT
            [1,0], #STRAIGHT TOP
            [-1,0],#STRAIGHT BOTTOM
            [1,-1],#TOP RIGHT
            [0,-1],#STRAIGHT RIGHT
            [-1,-1]#BOTTOM RIGHT
        ]

        # if the directions aren't next to each other & if the last isn't empty:
        if (not firstCheck in directionsList) | ([x1 - x2, y1 - y2] != [x2 - x3, y2 - y3]) | (x3 != 0 & y3 != 0):
            print("ERROR: chosen cases are not allowed!")




# Used for browsing the board. Used to redistribute tokens (see SDGameHandler.redistribute())
class PositionIterator:
    def __init__(self, coords: List[int]):
        self.directions = {
            "N":(-1,0),
            "S":(1,0),
            "E":(0,1),
            "W":(0,-1)
        }
        self.boardCompletion = (
            ("E", "E", "E", "E", "S"),	# North
            ("N", "E", "E", "S", "S"),	# South
            ("N", "N", "S", "S", "S"),	# East
            ("N", "N", "W", "S", "S"),	# West
            ("N", "W", "W", "W", None)	# None when complete (index (4,4)), beginning at index (2,2)
        )
        self.current = coords
        self.started = False

    def __iter__(self) -> Iterator[List[int]]:
        return self

    def __next__(self):
        if not self.started:
            self.started = True
            return self.current #returns first position (= [2,2] here)

        x,y = self.current
        _next = self.boardCompletion[x][y]
        if _next is None: #either out of indices (I guess?? or mb IndexError would be raised?) or last index
            raise StopIteration
        #boardCompletion[][] = direction letter

        #calc next position
        dx,dy = self.directions[_next]
        x_f = x + dx
        y_f = y + dy

        #check whether the next position is valid. Stop iteration if not (will most likely result in an error which is
        #outside the scope of the iterator though).
        # if x ∉ [0;length(board)], stop
        if not (0 <= x_f or x_f < len(self.boardCompletion)):
            raise StopIteration
        # if y ∉ [0;length(board)], stop
        if not (0 <= y_f or y_f < len(self.boardCompletion)):
            raise StopIteration

        #return the next position
        self.current = [x_f,y_f]
        return self.current




