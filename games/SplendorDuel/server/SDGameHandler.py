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
from wcwidth import wcswidth
from re import compile

from .Inventory import Inventory
from .Card import Card



ansi_escape = compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')  # used to avoid miscounting characters w/ self.strip_ansi()

# list of coordinates for the path in the board
# it has been generated with BoardPositionsPath.py
Path = [(2, 2), (3, 2), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3), (4, 2), (4, 1), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]


class SDGameHandler:
    """contains the data of the game, and the methods to check if a move is legal"""
    def __init__(self):

        # 5*5 matrix for the board.
        # On each case of the board, there may be a token
        self.board = [
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None]
        ]

        # empty inventories for the two players
        self.inventories = [Inventory(), Inventory()]

        # load the cards from the JSON file
        with open("cards/data.json", "r") as file:
            data = load(file)
        self.decks = [[Card(**card) for card in data["level" + str(l + 1)]] for l in range(3)]
        # and shuffle each deck
        for i in range(3):
            shuffle(self.decks[i])
            for c in self.decks[i]:
                print("\n".join(c.cardDraw(True)))



        # The same for the Royal Cards
        self.royalCards = [Card(**card) for card in data["royal"]]
        for c in self.royalCards:
            print("\n".join(c.cardDraw(True)))


            # distribute cards to the pyramid
        self.pyramid = [
            [self.decks[0].pop() for _ in range(5)], #list[JewelCard], #level 1 cards
            [self.decks[1].pop() for _ in range(4)], #list[JewelCard], #level 2 cards
            [self.decks[2].pop() for _ in range(3)]  #list[JewelCard]  #level 3 cards
        ]

        # prepare the bank (of tokens) and distribute them to the board
        self.bank = [PEARL,]*2 + [GOLD,]*3 + [BLUE_SAPPHIRE,]*4 + [DIAMOND,]*4 + [EMERALD,]*4 + [RUBY,]*4 + [OBSIDIAN,]*4
        self.distribute()



    def distribute(self) -> None:
        """distribute the remaining token on the board"""
        # shuffle the bank
        shuffle(self.bank)

        # browse the board according to the Path
        for x, y in Path:
            if self.board[x][y] is None and self.bank:
                self.board[x][y] = self.bank.pop()


    def strip_ansi(self, text: str) -> str:
        """
        used for deleting the escape sequence of colors (added w/ Fore, Back & Style)
        """
        return ansi_escape.sub('', text)


    def pad_to_width(self, s: str, width: int) -> str:
        """
        Used for padding two texts to a certain width (self.strPlayerDisplay)
        """
        visual_len = wcswidth(self.strip_ansi(s))
        padding = width - visual_len
        return s + ' ' * max(0, padding)


    def alignStrCards(self, cards: List[Card], emoji: bool) -> List[str]:
        """
        Method that returns a list of strs of the cards, but aligned.
        """
        cardStrList = [
            "",
            "",
            "",
            "",
            "",
            "",
            ""
        ]
        for i in range(len(cards)):
            try:
                for j in range(len(cards[i].cardDraw(emoji))):
                    cardStrList[j] += cards[i].cardDraw(emoji)[j]
            except AttributeError:
                if cards[i] is None:
                    cardStrList[0] += "┌───────────┐"
                    for j in range(5):
                        cardStrList[j+1] += "│           │"
                    cardStrList[6] += "└───────────┘"

        return cardStrList


    def strPyramid(self, emoji: bool = True) -> str:
        """
                  Returns the pyramid of cards as a string.
        /!\ Should only be used if the pyramid is already filled! /!\
        """
        lines = [[],[],[]]
        level = 0
        for x in self.pyramid:
            for i in range(len(x)): #level
                for j in range(len(x[i].cardDraw(emoji))): #line
                    try:
                        lines[level][j] += x[i].cardDraw(emoji)[j]

                    except IndexError:
                        lines[level].append(x[i].cardDraw(emoji)[j])
            level += 1
        strp = str()
        for i in range(len(lines)):
            for x in lines[i]:
                if i == 1:
                    strp += f"      " + x + "       \n"
                elif i == 2:
                    strp += "            " + x + "              \n"
                else:
                    strp += x + "\n"
        return strp


    def strInventory(self, player: int, isPlayer: bool, emoji: bool) -> str:
        """
        returns the str of an inventory.
        player      : number of the player (1 or 2)
        isPlayer    : displays the booked cards (if any)
        emoji       : prints w/ emojis if True, prints w/ console colors if False
        """
        if not (0 < player < 3):
            print(f"ERROR: Player should be 1 or 2! (Got player = {player})")
            return ""
        else:
            player -= 1

        strInv = str()

        if isPlayer:
            strU = " (you)"
            strBottom = str()
            alignedCards = self.alignStrCards(self.inventories[player].bookedCards, emoji)
            match len(self.inventories[player].bookedCards):
                case 0:
                    strBottom = f"└──────────────────────────────────────────────────────────┘"
                case 1:
                    space = "                                            "
                    for x in alignedCards:
                        strBottom += f"│ {x}{space}│\n"
                    strBottom += f"└──────────────────────────────────────────────────────────┘"
                case 2:
                    space = "                               "
                    for x in alignedCards:
                        strBottom += f"│ {x}{space}│\n"
                    strBottom += f"└──────────────────────────────────────────────────────────┘"
                case 3:
                    space = "                  "
                    for x in alignedCards:
                        strBottom += f"│ {x}{space}│\n"
                    strBottom += f"└──────────────────────────────────────────────────────────┘"

        else:
            strU = "──────"
            strBottom = f"└──────────────────────────────────────────────────────────┘"


        if emoji:
            if self.inventories[player].nbPrestige(-1) >= 10:
                nbPP = f"{self.inventories[player].nbPrestige(-1)},"
            else:
                nbPP = f" {self.inventories[player].nbPrestige(-1)}, "
            strInv += f"┌──────────────────────PLAYER {player + 1}{strU}──────────────────────┐\n"
            strInv += f"│ - Tokens        :     {tokenEmojis[0][1]}{self.inventories[player].tokens[1]}, {tokenEmojis[0][2]}{self.inventories[player].tokens[2]}, {tokenEmojis[0][3]}{self.inventories[player].tokens[3]}, {tokenEmojis[0][4]}{self.inventories[player].tokens[4]}, {tokenEmojis[0][5]}{self.inventories[player].tokens[5]}, {tokenEmojis[0][6]}{self.inventories[player].tokens[6]}, {tokenEmojis[0][7]}{self.inventories[player].tokens[7]}  │\n"
            strInv += f"│ - Cards (jewels):               {tokenEmojis[1][BLUE_SAPPHIRE]}{self.inventories[player].nbJewelCards(BLUE_SAPPHIRE)}, {tokenEmojis[1][DIAMOND]}{self.inventories[player].nbJewelCards(DIAMOND)}, {tokenEmojis[1][EMERALD]}{self.inventories[player].nbJewelCards(EMERALD)}, {tokenEmojis[1][RUBY]}{self.inventories[player].nbJewelCards(RUBY)}, {tokenEmojis[1][OBSIDIAN]}{self.inventories[player].nbJewelCards(OBSIDIAN)}  │\n"
            strInv += f"│ - Prestige      : Total:{nbPP} {tokenEmojis[1][None]}{self.inventories[player].nbPrestige(None)},{tokenEmojis[1][BLUE_SAPPHIRE]}{self.inventories[player].nbPrestige(BLUE_SAPPHIRE)}, {tokenEmojis[1][DIAMOND]}{self.inventories[player].nbPrestige(DIAMOND)}, {tokenEmojis[1][EMERALD]}{self.inventories[player].nbPrestige(EMERALD)}, {tokenEmojis[1][RUBY]}{self.inventories[player].nbPrestige(RUBY)}, {tokenEmojis[1][OBSIDIAN]}{self.inventories[player].nbPrestige(OBSIDIAN)}  │\n"
            strInv += f"│ - Privileges    : {itemsEmoji[items[4]]} {self.inventories[player].nbPrivileges}                                   │\n"
            strInv += f"│ - Crowns        : {itemsEmoji[items[3]]} {self.inventories[player].nbCrowns()}                                   │\n"
            strInv += f"│ - Booked cards  : {len(self.inventories[player].bookedCards)}                                      │\n"
            strInv += strBottom + "\n"
        else:
            if self.inventories[player].nbPrestige(-1) >= 10:
                nbPP = f"{self.inventories[player].nbPrestige(-1)},"
            else:
                nbPP = f" {self.inventories[player].nbPrestige(-1)}, "
            strInv += f"┌──────────────────────PLAYER {player + 1}{strU}──────────────────────┐\n"
            strInv += f"│ - Tokens        :      {tokenEmojis[2][1]}{self.inventories[player].tokens[1]}{tokenColors[0]},  {tokenEmojis[2][2]}{self.inventories[player].tokens[2]}{tokenColors[0]},  {tokenEmojis[2][3]}{self.inventories[player].tokens[3]}{tokenColors[0]},  {tokenEmojis[2][4]}{self.inventories[player].tokens[4]}{tokenColors[0]},  {tokenEmojis[2][5]}{self.inventories[player].tokens[5]}{tokenColors[0]},  {tokenEmojis[2][6]}{self.inventories[player].tokens[6]}{tokenColors[0]},  {tokenEmojis[2][7]}{self.inventories[player].tokens[7]}{tokenColors[0]}  │\n"
            strInv += f"│ - Cards (jewels):                {tokenEmojis[2][BLUE_SAPPHIRE]}{self.inventories[player].nbJewelCards(BLUE_SAPPHIRE)}{tokenColors[0]},  {tokenEmojis[2][DIAMOND]}{self.inventories[player].nbJewelCards(DIAMOND)}{tokenColors[0]},  {tokenEmojis[2][EMERALD]}{self.inventories[player].nbJewelCards(EMERALD)}{tokenColors[0]},  {tokenEmojis[2][RUBY]}{self.inventories[player].nbJewelCards(RUBY)}{tokenColors[0]},  {tokenEmojis[2][OBSIDIAN]}{self.inventories[player].nbJewelCards(OBSIDIAN)}{tokenColors[0]}  │\n"
            strInv += f"│ - Prestige      : Total:{nbPP} {tokenEmojis[2][None]}{self.inventories[player].nbPrestige(None)}{tokenColors[0]}, {tokenEmojis[2][BLUE_SAPPHIRE]}{self.inventories[player].nbPrestige(BLUE_SAPPHIRE)}{tokenColors[0]},  {tokenEmojis[2][DIAMOND]}{self.inventories[player].nbPrestige(DIAMOND)}{tokenColors[0]},  {tokenEmojis[2][EMERALD]}{self.inventories[player].nbPrestige(EMERALD)}{tokenColors[0]},  {tokenEmojis[2][RUBY]}{self.inventories[player].nbPrestige(RUBY)}{tokenColors[0]},  {tokenEmojis[2][OBSIDIAN]}{self.inventories[player].nbPrestige(OBSIDIAN)}{tokenColors[0]}  │\n"
            strInv += f"│ - Privileges    : {self.inventories[player].nbPrivileges}                                      │\n"
            strInv += f"│ - Crowns        : {self.inventories[player].nbCrowns()}                                      │\n"
            strInv += f"│ - Booked cards  : {len(self.inventories[player].bookedCards)}                                      │\n"
            strInv += strBottom + "\n"

        return strInv


    def strRoyalCards(self, emoji:bool) -> str:
        strList = self.alignStrCards(self.royalCards, emoji)
        strReturn = str()
        for x in strList:
            strReturn += x + "\n"
        return strReturn


    def strPlayerDisplay(self,player: int, emoji:bool) -> str:
        if not (0 < player < 3):
            print(f"ERROR: Player should be 1 or 2! (Got player = {player})")
            return ""
        else:
            player -= 1

        #Pyramid + Royal Cards
        strRet1 =  "┌───────────────────────────────────────────────────────────────┐\n"
        strRet1 += "│                 Available cards on the board                  │\n"
        strRet1 += "└───────────────────────────────────────────────────────────────┘\n"
        strRet1 += self.strPyramid(emoji)
        strRet1 += "┌───────────────────────────────────────────────────────────────┐\n"
        strRet1 += "│                     Available Royal Cards                     │\n"
        strRet1 += "└───────────────────────────────────────────────────────────────┘\n"

        # The following lines are used to recentre 4 Royal Cards w/ the textbox just above
        for x in self.strRoyalCards(emoji).splitlines():

            strRet1 += ((4-len(self.royalCards)) * "      "     #used for "dynamic" shifting i.e. depending on the amnt of cards available
                        + "      " + x + "\n")                  #used for shifting
            #Kind of outdated considering we now always have 4 elements in the list but the shifting still works

        # Writes the inventory (depending on `player`)
        if player:
            strRet2 =  self.strInventory(2, True, emoji) + "\n"
            strRet2 += self.strInventory(1, False, emoji)
            strRet2 += self.strBoard(emoji)
        else:
            strRet2 =  self.strInventory(1, True, emoji) + "\n"
            strRet2 += self.strInventory(2, False,emoji)
            strRet2 += self.strBoard(emoji)



        ##⚠️⚠️⚠️⚠️ if WCSWidth isn't / can't be installed, just de-comment the next line and comment the next ones. (display will be slightly less pretty although usable)
        ##return strRet1 + strRet2


        # ⚠️⚠️⚠️⚠️ if WCSWidth isn't / can't be installed, comment the next lines until the return statement
        # Combining those blocks
        block1 = strRet1.splitlines()
        block2 = strRet2.splitlines()

        block1 = [line.rstrip() for line in block1]     # to remove spaces at the end of each line
        maxLength = max(wcswidth(self.strip_ansi(line)) for line in block1)

        # adding space to other lines when required
        block1 = [self.pad_to_width(line, maxLength) for line in block1]

        # adding empty vertical lines if the block is shorter
        maxLines = max(len(block1), len(block2))
        block1 += [self.pad_to_width('', maxLength)] * (maxLines - len(block1))     # "[' ' * maxLength] is a line; (maxLength-len(block1)) is the amnt of [] lines added
                                                                                    # so basically we add spaces to shift the other block's lines
        block2 += [''] * (maxLines - len(block2))

        lstRet = [line1 + "  " + line2 for line1,line2 in zip(block1,block2)]   # appends lines of block 2 to lines of block 1
        return "\n".join(lstRet)                                                # returns a string w/ "\n" between all the lines


    def strBoard(self, emoji: bool) -> str:
        """
        Returns a string (with multiple "\n") to display the board (useful for `strPlayerDisplay()`)
        """
        # header display
        strRet =  "┌──────────────────────────────────────────────────────────┐\n"
        strRet += "│                          BOARD                           │\n"
        strRet += "└──────────────────────────────────────────────────────────┘\n"

        # Board
        if emoji:
            # to align the board display w/ the header
            alignmentSpace = "                      " # 22 spaces
            strRet += alignmentSpace + "┌────────────┐" + "\n" #top of the board
            for x in self.board:
                strRet += alignmentSpace + "│ " # left side of the board
                for i in range(len(x)):
                    if x[i] is None:
                        strRet += "🕳️"
                    else:
                        strRet += tokenEmojis[emoji][x[i]]
                    if i == 4:
                        strRet += " │\n" # right side of the board
            strRet += alignmentSpace + "└────────────┘" #bottom of the board

        else:
            # to align the board display w/ the header (Emojis take more space than colored letters)
            alignmentSpace = "                       " # 23 spaces
            strRet += alignmentSpace + "┌───────────┐" + "\n" #top of the board
            for x in self.board:
                strRet += alignmentSpace + "│ " # left side of the board
                for i in range(len(x)):
                    if x[i] is None:
                        strRet += ". "
                    else:
                        strRet += tokenEmojis[emoji][x[i]] + Fore.RESET + " "
                    if i == 4:
                        strRet += "│\n" # right side of the board
            strRet += alignmentSpace + "└───────────┘" #bottom of the board

        return strRet


    def addToInventory(self, player: int, itemType: int, item: Card | int | list) -> None:
        """
        Adds some item(s) in a player's inventory

        itemType: see constants.py (n.b. use BOOKED_CARD to book a card... yeah I shouldn't have used the past principle)
        item    : JewelCard, RoyalCard (not yet created), list[tokenType, tokenAmount] or int (if privilege)

        """
        # Jewel Card
        # Token
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
                self.chooseRoyalCard(player,item)
            case 4: #PRIVILEGE 🗞️
                #item should be 1 or -1
                if item == 1:
                    self.getPrivilegeScroll(player)
                elif item == -1:
                    self.usePrivilegeScroll(player)
                else:
                    print(f"ERROR: Players can only receive or lose one privilege at a time!")
                    return

                if self.inventories[player].nbPrivileges > 3:
                    print(f"ERROR: Player {player + 1} has {self.inventories[player].nbPrivileges} privileges!")
                elif self.inventories[player].nbPrivileges <= -2:
                    print(f"ERROR: Player {player + 1} has {self.inventories[player].nbPrivileges} privileges!")    # Plural if x ∈ ℝ\{(-2;2)}...
                elif self.inventories[player].nbPrivileges < 0:
                    print(f"ERROR: Player {player + 1} has {self.inventories[player].nbPrivileges} privilege!")     # ...otherwise, singular
            case _:
                print("ERROR: itemType unrecognised!")


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
                    self.board[x[0]][x[1]] = None

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


    def getPrivilegeScroll(self,player) -> None:
        """
        Checks whether the player can receive a privilege scroll.
        If yes, checks whether it takes it from the opponent (which case all three of them should be dispatched among players)
        or takes it from the board.
        """
        if not (0 < player < 3):
            print(f"ERROR: Player should be 1 or 2! (Got player = {player})")
        else:
            player -= 1

        #you're not eligible if you have already all the privilege scrolls
        if self.inventories[player].nbPrivileges == 3:
            #cant get privilege
            return

        #if there is no privilege scroll on the board anymore...
        elif self.inventories[player-1].nbPrivileges + self.inventories[player].nbPrivileges == 3:
            #...we check whether the opponent has one (they should), which case we steal one from them to add to the other player
            if  self.inventories[player-1].nbPrivileges != 0:
                self.inventories[player-1].nbPrivileges -= 1
                self.inventories [player] .nbPrivileges += 1

        #And if there is still some privilege scrolls on the board...
        else:
            #we can distribute one to the player
            self.inventories[player].nbPrivileges += 1


    def usePrivilegeScroll(self,player):
        """
        Checks whether a player can use a privilege.
        If yes, the method moves the privilege towards the board.
        If no, the game ends.
        """
        if not (0 < player < 3):
            print(f"ERROR: Player should be 1 or 2! (Got player = {player})")
        else:
            player -= 1

        if self.inventories[player].nbPrivileges <= 0:
            print("ERROR: player {player+1} hasn't got any privilege!")
            return
        else:
            self.inventories[player].nbPrivileges -= 1
            return


    def chooseRoyalCard(self,player: int, card: Card):
        """
        Gets a royal card inside the inventory of a player.
        Must be used whenever needed, i.e. whenever a player reaches 3 crowns or 6 crowns.

        (On second thought: Maybe we should use either indices of the self.royalCards list
        instead of RoyalCard objects since we're going to use it w/ game.royalCards[n]...)
        """
        if card is None:
            print("ERROR: Impossible to get RoyalCard! (card is a None object)")
            return
        elif not (card in self.royalCards):
            print("ERROR: Impossible to get RoyalCard!")
            return
        else:
            self.inventories[player].chooseRoyalCard(card)
            self.royalCards[self.royalCards.index(card)] = None
            return


    def buyBookedCard(self, player: int, cardIndex: int) -> None:
        """
        Lets a player buy a JewelCard they previously booked using the cardIndex.
        cardIndex is the index within the Inventory.bookedCards list.
        """
        if not(1 <= player <= 2):
            print(f"ERROR: unrecognised player (should be 1 or 2, got {player} instead!)")
        else:
            player -= 1

        self.addToInventory(player+1,JEWEL_CARD, self.inventories[player].bookedCards.pop(cardIndex))



