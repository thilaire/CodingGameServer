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
from random import randint, seed, shuffle
from json import load

from .Inventory import Inventory
from .JewelCard import JewelCard
from .RoyalCard import RoyalCard

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

        self.inventories = [Inventory(), Inventory()]
        self.decks = [
            [], #level 1 cards
            [], #level 2 cards
            [] #level 3 cards
        ]
        self.pyramid = [
            [], #list[JewelCard], #level 1 cards
            [], #list[JewelCard], #level 2 cards
            []  #list[JewelCard]  #level 3 cards
        ]
        self.royalCards = []

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

        # [None, [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], 0, 0]
        # [jewel_card , token]
        for gemstone in range(1,8):
            countedTokens[gemstone] += self.inventories[0].nbTokens(gemstone) #TODO
            countedTokens[gemstone] += self.inventories[1].nbTokens(gemstone) #TODO

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


    def loadDecks(self) -> None:
        # Taken from `WillItCrash.py`:
        with open("cards/data.json", "r") as file:
            data = load(file)

        self.decks[0] = [JewelCard(**card) for card in data["level1"]]
        self.decks[1] = [JewelCard(**card) for card in data["level2"]]
        self.decks[2] = [JewelCard(**card)for card in data["level3"]]
        # will probably have to do the same for Royal Cards, something like:
        self.royalCards = [RoyalCard(**card)for card in data["royal"]]


        # # to print in debug, not in clear
        # print()
        # print("Level 1 :")
        # for x in self.decks[0]:
        #     print(x)
        # print()
        # print("Level 2: ")
        # for x in self.decks[1]:
        #     print(x)
        # print()
        # print("Level 3: ")
        # for x in self.decks[2]:
        #     print(x)
        # print()
        # print("Royal: ")
        # for x in self.royalCards:
        #     print(x)

    def shuffleDecks(self) -> None:
        shuffle(self.decks[0])
        shuffle(self.decks[1])
        shuffle(self.decks[2])


    def loadPyramid(self) -> None:
        for i in range(5):
            self.pyramid[0].append(self.decks[0].pop())
        for i in range(4):
            self.pyramid[1].append(self.decks[1].pop())
        for i in range(3):
            self.pyramid[2].append(self.decks[2].pop())

    def printPyramid(self, emoji: bool = True) -> None:
        """
                        Prints the pyramid of cards.
        /!\ Should only be used if the pyramid is already filled! /!\
        """
        lines = [[],[],[]]
        #lvl3lines += [x.cardDraw() for x in self.pyramid[2]]

        # for x in self.pyramid[2]:
        #     for y in x.cardDraw():
        #         try:
        #             lvl3lines[x.cardDraw().index(y)] += y
        #         except IndexError:
        #             lvl3lines.append(y)
        level = 0
        for x in self.pyramid:
            for i in range(len(x)): #level
                for j in range(len(x[i].cardDraw(emoji))): #line
                    try:
                        lines[level][j] += x[i].cardDraw(emoji)[j]

                    except IndexError:
                        lines[level].append(x[i].cardDraw(emoji)[j])
            level += 1

        for i in range(len(lines)):
            for x in lines[i]:
                if i == 1:
                    temp = "      " + x
                    print(temp)
                elif i == 2:
                    temp = "            " + x
                    print(temp)
                else:
                    print(x)


    def printInventory(self, player: int, isPlayer: bool, emoji: bool):
        """
        Prints an inventory.
        player      : number of the player (1 or 2)
        isPlayer    : displays the booked cards (if any)
        emoji       : prints w/ emojis if True, prints w/ console colors if False
        """
        if not (0 < player < 3):
            print(f"ERROR: Player should be 1 or 2! (Got player = {player})")
            return
        else:
            player -= 1
        strU = "──────"
        if isPlayer:
            strU = " (you)"
        if emoji:
            print(f"┌──────────────────────PLAYER {player}{strU}──────────────────────┐")
            print(f"│ - Tokens        :     {tokenEmojis[0][1]}{self.inventories[player].tokens[1]}, {tokenEmojis[0][2]}{self.inventories[player].tokens[2]}, {tokenEmojis[0][3]}{self.inventories[player].tokens[3]}, {tokenEmojis[0][4]}{self.inventories[player].tokens[4]}, {tokenEmojis[0][5]}{self.inventories[player].tokens[5]}, {tokenEmojis[0][6]}{self.inventories[player].tokens[6]}, {tokenEmojis[0][7]}{self.inventories[player].tokens[7]}  │")
            print(f"│ - Cards (jewels):               {tokenEmojis[1][BLUE_SAPPHIRE]}{self.inventories[player].nbJewelCards(BLUE_SAPPHIRE)}, {tokenEmojis[1][DIAMOND]}{self.inventories[player].nbJewelCards(DIAMOND)}, {tokenEmojis[1][EMERALD]}{self.inventories[player].nbJewelCards(EMERALD)}, {tokenEmojis[1][RUBY]}{self.inventories[player].nbJewelCards(RUBY)}, {tokenEmojis[1][OBSIDIAN]}{self.inventories[player].nbJewelCards(OBSIDIAN)}  │")
            print(f"│ - Prestige      : Total: {self.inventories[player].nbPrestige(-1)}, {tokenEmojis[1][None]}{self.inventories[player].nbPrestige(None)},{tokenEmojis[1][BLUE_SAPPHIRE]}{self.inventories[player].nbPrestige(BLUE_SAPPHIRE)}, {tokenEmojis[1][DIAMOND]}{self.inventories[player].nbPrestige(DIAMOND)}, {tokenEmojis[1][EMERALD]}{self.inventories[player].nbPrestige(EMERALD)}, {tokenEmojis[1][RUBY]}{self.inventories[player].nbPrestige(RUBY)}, {tokenEmojis[1][OBSIDIAN]}{self.inventories[player].nbPrestige(OBSIDIAN)}  │")
            print(f"│ - Privileges    : {itemsEmoji[items[4]]} {self.inventories[player].nbPrivileges}                                   │")
            print(f"│ - Crowns        : {itemsEmoji[items[3]]} {self.inventories[player].nbCrowns()}                                   │")
            print(f"│ - Booked cards  : {len(self.inventories[player].bookedCards)}                                      │")
    def addToInventory(self, player: int,  itemType: int, item: JewelCard | RoyalCard | int | list) -> None:
        # TODO
        #   Substitution of any token for a gold one (when buying a card for instance)
        #   idea: count every token required for a card. If there isn't enough, count gold tokens, and add them to those
        #   uncompleted. If there's still not enough, then it's illegal.
        # I think it's handled directly in `Inventory.buyJewelCard()`??? I don't remember...
        """
        Adds some item(s) in a player's inventory

        itemType: see constants.py
        item    : JewelCard, RoyalCard (not yet created), list[tokenType, tokenAmount] or int (if privilege)
        """
        # Jewel Card
        # Token
        # Crown
        # TODO I guess
        #   !! when reaching 3 or 6 crowns
        #   call a new method, "chooseRoyalCard()" or smth
        # Privilege Scrolls

        if not(0 <= player - 1 <= 1):
            print("ERROR: unrecognised player (should be 1 or 2)")
        else:
            player -= 1

        #add stuff to the inventory + checks
        match itemType:
            case 0: #TOKEN 🪙
                if not isinstance(item, list):
                    print(f"ERROR: item wrongly formatted! (expected list[tokenType, tokenAmount], got {item})")
                else:
                    self.inventories[player].addToken(item[0],item[1])
            case 1: #JEWEL_CARD 💎
                self.inventories[player].buyJewelCard(item)
            case 2: #BOOKED_CARD 🎟️
                self.inventories[player].bookCard(item)
            case 3: #ROYAL_CARD 👑
                self.inventories[player].chooseRoyalCard(item)
            case 4: #PRIVILEGE 🗞️
                self.inventories[player].nbPrivileges += item
                if self.inventories[player].nbPrivileges > 3:
                    print(f"ERROR: Player {player + 1} has {self.inventories[player].nbPrivileges} privileges!")
                elif self.inventories[player].nbPrivileges <= -2:
                    print(f"ERROR: Player {player + 1} has {self.inventories[player].nbPrivileges} privileges!")    # Plural if x ∈ ℝ\{(-2;2)}...
                elif self.inventories[player].nbPrivileges < 0:
                    print(f"ERROR: Player {player + 1} has {self.inventories[player].nbPrivileges} privilege!")     # ...otherwise, singular
            case _:
                print("ERROR: itemType unrecognised!")

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
    def tokenCapture(self,coords: list[list], player: int) -> None:
        """
        checks whether the list of coordinates given is legit. (<4 elements in the list, all following each other in vertical,
        horizontal or diagonal, with two elements in each coordinate i.e. [x, y]).
        Then we check whether there's a gold token, which case the move is illegal.
        Then we check whether the three tokens are identical, or whether there's two pearls chosen, which case the
        opponent gets a privilege scroll.
        """

        if len(coords) > 3:
            print("ERROR: You can only capture 3 tokens at most!")
            return

        if not(0 <= player - 1 <= 1):
            print("ERROR: unrecognised player (should be 1 or 2)")
            return
        else:
            player -= 1

        # Getting the coordinates in variables
        points = list()
        #p1
        try:
            x1, y1 = coords[0] #p1
            points.append(coords[0])
            if (not(type(x1) is int)) or (not(type(y1) is int)):
                print(f"ERROR: expected int coordinates in this format: [ [x1,y1], [x2,y2], [x3,y3] ] or [-1,-1] if not selected. Got {coords} instead!")
                return
        except IndexError:
            print(f"ERROR: You should capture at least one token! (first token coordinates not given)")
            return
        except ValueError:  #e.g. here:
                            # testList = [1,2,3]
                            # a,b = testList
                            #this leads to a ValueError like this:
                            #"ValueError: too many values to unpack (expected 2)"
            print(f"ERROR: wrong coordinates format! (expected [ [x1,y1], [x2,y2], [x3,y3] ], [-1,-1] if not selected. Got {coords} instead!)")
            return

        if coords[0] == [-1,-1]:
            print(f"ERROR: You should capture at least one token! (first token coordinates not given)")
            return


        #p2
        try:
            x2, y2 = coords[1] #Try/Catch IndexError if they're not given
            points.append(coords[1])
            if (not(type(x2) is int)) or (not(type(y2) is int)):
                print(f"ERROR: expected int coordinates in this format: [ [x1,y1], [x2,y2], [x3,y3] ] or [-1,-1] if not selected. Got {coords} instead!")
                return
        except IndexError:
            x2,y2 = -1,-1
            points.append([-1, -1])
        except ValueError:
            print(f"ERROR: wrong coordinates format! (expected [ [x1,y1], [x2,y2], [x3,y3] ], [-1,-1] if not selected. Got {coords} instead!)")
            return

        #p3
        try:
            x3, y3 = coords[2] #Same idea here
            points.append(coords[2])
            if (not(type(x3) is int)) or (not(type(y3) is int)):
                print(f"ERROR: expected int coordinates in this format: [ [x1,y1], [x2,y2], [x3,y3] ] or [-1,-1] if not selected. Got {coords} instead!")
                return
        except IndexError:
            x3, y3 = -1, -1
            points.append([-1, -1])
        except ValueError:
            print(f"ERROR: wrong coordinates format! (expected [ [x1,y1], [x2,y2], [x3,y3] ], [-1,-1] if not selected. Got {coords} instead!)")
            return

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

        #checking whether the positions are valid (vertical, horizontal, diagonal)
        # -1: Error (shouldn't happen); 1: p1 is given; 2: p1 & p2 are given; 3: all are given
        # I think it's useless actually...
        _case = -1

        #Checking how many tokens are being captured (i.e. how many we should check)
        if x3 == -1 & y3 == -1:     #3rd one empty
            if x2 == -1 & y2 == -1: #2nd one empty & <= 1 coordinate given (0 shouldn't be possible though)
                _case = 1
                d_coords1   = []
                d_coords2   = []
            else:                   #3rd one empty & <= 2 coordinate(s) given.
                _case = 2
                # d_coords1 calculation
                d_coords1   = [x1 - x2, y1 - y2]
                d_coords2   = []
        else:   # d_coordsN calculations (will be useful to check directions)
            _case = 3
            d_coords1       = [x1 - x2, y1 - y2]
            d_coords2       = [x2 - x3, y2 - y3]

        # checking whether the positions are valid (vertical, horizontal, diagonal) i.e. whether they're in the same direction
        # use d_coordsN + directionsList
        if len(d_coords1) == 2:
            if not(d_coords1 in directionsList):
                print(f"ERROR: tokens are not aligned!")
                return
            else:
                if len(d_coords2) == 2:
                    if d_coords1 != d_coords2:
                        print("ERROR: tokens are not aligned!")
                        return


        # Checking whether they're capturing nothing or a gold token, which case they lose.
        # + adding & counting the tokens w/ listCount
        # use: listCount[TOKEN_TYPE-1] because None doesn't exist in this list.
        # TOKEN_TYPE: int constants (see file `Constants.py`, l.39-45 [no pun intended: l.38 ("None") is unused here])
        listCount = [0,0,0,0,0,0,0] #Note: dictionary would've been better. My bad

        for x in points:
            if x[0] < 0 or x[1] < 0:
                if x != [-1,-1]:
                    print(f"ERROR: invalid indices! (expected coordinates within the board or [-1,-1], got {x} instead!)")
                    return
                else:
                    #just here to tell us that there is nothing, so we get out of the loop since the next should also be [-1,-1].
                    break
            elif x[0] > 4 or x[1] > 4:
                print(f"ERROR: invalid indices! (expected coordinates within the board or [-1,-1], got {x} instead!)")
                return
            elif self.board[x[0]][x[1]] is None:
                print("ERROR: Tried to capture an empty board case!")
                return
            else:
                if self.board[x[0]][x[1]] == GOLD:
                    print("ERROR: Tried to capture a gold token!")
                else:
                    # place tokens in the inventory
                    self.inventories[player].addToken(self.board[x[0]][x[1]], 1)
                    listCount[ self.board [x[0]] [x[1]] - 1] += 1
                    # replace tokens on the board
                    self.update_board(None, x)

        # Checking whether they're capturing two pearls or three gemstones
        if listCount[0] == 2:
            # Selected 2 pearls.
            print(f"INFO: Opponent receives a privilege scroll! (two {tokenTypes[1]} tokens selected!)")
            return
        else:
            # Selected 3 gemstones.
            for i in range(len(listCount)):
                if listCount[i] == 3:
                    print(f"INFO: Opponent receives a privilege scroll! (three {tokenTypes[i+1]} tokens selected!)")
            return



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




