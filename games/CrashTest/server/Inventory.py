from dataclasses import dataclass, field
from typing import List

from .Constants import * #really needed?
from .JewelCard import JewelCard

@dataclass
class Inventory:
    _nbPrivileges   : int
    tokens          : list[int|None] = field(default_factory = lambda :
        [None, 0, 0, 0, 0, 0, 0, 0])
    jewelCards      : dict = field(default_factory = lambda :{
        None            : list[JewelCard],
        BLUE_SAPPHIRE   : list[JewelCard],
        DIAMOND         : list[JewelCard],
        EMERALD         : list[JewelCard],
        RUBY            : list[JewelCard],
        OBSIDIAN        : list[JewelCard]
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
        self.jewelCards[temp.tokenType].append(temp)

        # to be replaced w/ this (see todo just above) :
        # self.jewelCards[jewelCard.tokenType].append(jewelCard)

    def buyJewelCard(self, player: int, card: JewelCard):
        # Sum every jewel from the cards we own
        dictSum = {
            # We'll sum up every jewel in a dict that's close to JewelCard.requirements to then add stuff into the former dict.
            PEARL           : 0,  # PEARL,
            BLUE_SAPPHIRE   : 0,  # SAPPHIRE,
            DIAMOND         : 0,  # DIAMOND,
            EMERALD         : 0,  # EMERALD,
            RUBY            : 0,  # RUBY,
            OBSIDIAN        : 0  # OBSIDIAN
        }
        # we sum up every JewelCard.nbJewel in the inventory.
        for cardType in self.jewelCards:
            if cardType is None:
                pass  # type none exists in jewel cards, not in requirements.
            else:
                dictSum[cardType] = sum(card.nbJewel for card in cardType)


        #check requirements for card (aka for each requirement of the card)
        #for each jewel of the card
        for reqJewel in card.requirements:
            if card.requirements[reqJewel] > dictSum[reqJewel]:
                # if they're not enough, we sum up the tokens & the jewels
                # and if they're still not enough, we raise an error
                if card.requirements[reqJewel] > dictSum[reqJewel] + self.tokens[reqJewel]:
                    print(f"ERROR: Not enough {tokenTypes[reqJewel]} jewels & tokens to buy JewelCard!")
                    return -1
                #in the other case, we just subtract the amount of tokens needed to purchase the card
                else:
                    self.tokens[reqJewel] -= card.requirements[reqJewel] - dictSum[reqJewel]
                #otherwise we subtract the tokens (we'll add to inventory once every token has been subtracted)
            #else:
                #otherwise we good
        #yeah thats it, we can add it to the inventory
        #nvm, we should check for special moves
        #first special move

        self.addJewelCard()

    def runAbility(self, ability: int):
        match ability:
            #0 i.e. nothing:
            case 0:
                #skip everything, don't even bother looking at the second index
                pass
            #Choose token:
            case CHOOSE_GEMSTONE:
                #we'll pop the JewelCard instance, change it, then add it to the inventory
            #Play again:
            case PLAY_AGAIN:
                #just call the play method/return the play code or smth, idk
            #Take a token:
            case TAKE_A_TOKEN:
                #something similar to SDGameHandler.tokenCapture()
            #Get a privilege:
            case GET_PRIVILEGE:
                #call the method, I believe the get a privilege stuff works the same regardless of the way you get one
            #steal token:
            case STEAL_GEMSTONE
                #check the opponents inventory, if the chosen token is there we subtract it, if not there'll be an error

    def chooseGemstone(self):
        #should it be in SDGameHandler?
        pass



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