from dataclasses import dataclass, field
from .Constants import * #really needed?
from .JewelCard import JewelCard

@dataclass
class Inventory:
    _nbPrivileges: int
    tokens: list[int|None] = field(default_factory = lambda : [None, 0, 0, 0, 0, 0, 0, 0])
    jewelCards: dict = field(default_factory = lambda :{
        None : list[JewelCard],
        BLUE_SAPPHIRE : list[JewelCard],
        DIAMOND : list[JewelCard],
        EMERALD : list[JewelCard],
        RUBY : list[JewelCard],
        OBSIDIAN : list[JewelCard]
    })



    #returns the number of jewels of a certain type
    def nbJewelCards(self, _type) -> int:
        """
        Returns the number of jewel cards of a specified type.
        """
        #go through all the cards, select every _type card, sum them.
        return sum(x.nbJewel for x in self.jewelCards if x.tokenType == _type)

    def nbTokens(self, _type):
        """
        Returns the amount of tokens of a specified type.
        """

    def addJewelCard(self, #jewelCard):
                     jewelCardsList, index):
        """
        pops jewelCardsList[index] to add it to the inventory.
        jewelCardsList is either the level 1, 2  or 3 deck.
        """
        #TODO: pop OUTSIDE of the method
        temp = jewelCardsList.pop(index)
        self.jewelCards[tokenTypesDict[temp.tokenType]].append(temp)

        # to be replaced w/ this (see todo just above) :
        # self.jewelCards[jewelCard.tokenType].append(jewelCard)




    def addToken(self, idToken, amount):
        if idToken is None:
            print("ERROR: Token \"None\" does not exist!")
        else:
            self.tokens[idToken] += amount
            if self.tokens[idToken] > maxTokenAmounts[tokenTypes[idToken]]:
                print(f"ERROR: Cannot have more than {maxTokenAmounts[tokenTypes[idToken]]} tokens of type {tokenTypes[idToken]}!")
                self.tokens[idToken] -= amount
            elif self.tokens[idToken] < -2:
                print(f"ERROR: Cannot have less than {maxTokenAmounts[tokenTypes[idToken]]} tokens of type {tokenTypes[idToken]}!")
                self.tokens[idToken] -= amount
            elif self.tokens[idToken] < 0:
                print(f"ERROR: Cannot have less than {maxTokenAmounts[tokenTypes[idToken]]} token of type {tokenTypes[idToken]}!")
                self.tokens[idToken] -= amount
            elif sum(x for x in self.tokens if x is not None) > 10:
                print(f"WARNING: You should have 10 tokens at most, you need to throw {sum(x for x in self.tokens if x is not None) - 10} of them!")
                #TODO: token management


    def nbPrestige(self, _type: int) -> int:
        """
        Returns the amount of prestige points.
        To get all the prestige points, _type should be -1.
        """
        #run through all the jewelCards colors;
        #run through all the cards;
        #sum up all the prestige points

        if _type == -1:
            return sum(card.nbPrestige for colorList in self.jewelCards.values() for card in colorList)
        else:
            try:
                return sum(card.nbPrestige for card in self.jewelCards[_type])
            except KeyError:
                print(f"ERROR: No such Jewel Card type ({_type}) exists!")
                return -1


    @property
    def nbPrivileges(self):
        """
        returns the amount of privileges
        """
        return self._nbPrivileges

    @nbPrivileges.setter
    def nbPrivileges(self, val):
        self._nbPrivileges = val