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

    def addJewelCard(self, jewelCard):
                     #jewelCardsList, index):
        """
        pops jewelCardsList[index] to add it to the inventory.
        jewelCardsList is either the level 1, 2  or 3 deck.
        """
        # #need to pop OUTSIDE the method
        # temp = jewelCardsList.pop(index)
        # self.jewelCards[temp.tokenType].append(temp)

        # to be replaced w/ this (see just above) :
        self.jewelCards[jewelCard.tokenType].append(jewelCard)

    def buyJewelCard(self, # player: int, #Nope, "player" selector will be in SDGameHandler
                     card: JewelCard):
        #Side-note: I've mixed "special moves" and "abilities" in last commits.
        #I've tried to "standardise" everything and use only "ability" / "special ability", but if there's one that
        #I didn't catch yet, or you're looking into previous commits, you now know.
        """
        Just checks whether we can add the card to the inventory.
        Returns a list in the following format: [playAgain: bool ; specialMove: int]
        playAgain   : whether we're playing again or not
        specialAbility : which one of the 5, if any. 0 if no special ability, -1 if acquiring failed (which case, error).

        (We'll handle the card special ability in either SDGameHandler or SplendorDuel, not sure yet.)
        """
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
                dictSum[cardType] = sum(card.nbJewel for card in self.jewelCards[cardType])

        #check requirements for card (aka for each requirement of the card)
        #for each jewel of the card
        for reqJewel in card.requirements:
            if card.requirements[reqJewel] > dictSum[reqJewel]:
                # if they're not enough, we sum up the tokens & the jewels
                # and if they're still not enough, we raise an error
                if card.requirements[reqJewel] > dictSum[reqJewel] + self.tokens[reqJewel]:
                    # We don't own enough tokens & jewels, so we're checking whether there's a gold token, which case we'll
                    # substitute the requirement for a gold token.
                    if card.requirements[reqJewel] > dictSum[reqJewel] + self.tokens[reqJewel] + self.tokens[GOLD]:
                        print(f"ERROR: Not enough {tokenTypes[reqJewel]} jewels & tokens to buy JewelCard!")
                        return [False,-1]
                    else:
                        #this should be negative I believe?
                        self.tokens[reqJewel] -= card.requirements[reqJewel] - dictSum[reqJewel]

                        # which case we add the negative number to the gold tokens, then put it to zero, then check whether
                        # there's anything in the tokens < 0 ?
                        self.tokens[GOLD] += self.tokens[reqJewel]
                        self.tokens[reqJewel] = 0
                #in the other case, we just subtract the amount of tokens needed to purchase the card
                else:
                    self.tokens[reqJewel] -= card.requirements[reqJewel] - dictSum[reqJewel]
                #otherwise we subtract the tokens (we'll add to inventory once every token has been subtracted)
            #else:
                #otherwise we good
        #yeah thats it, we can add it to the inventory

        # checking whether we have a negative amount of any token
        for i in range(len(self.tokens)):
            if self.tokens[i] is None:
                pass
            elif self.tokens[i] < 0:
                print(f"ERROR: Negative amount of token! ({tokenTypes[i]} = {self.tokens[i]}")
                return [False, -1]


        self.addJewelCard(card)
        #then we should check for special ability and return them
        firstReturn = False
        if card.abilities[0] == PLAY_AGAIN or card.abilities[1] == PLAY_AGAIN:
            firstReturn = True

        #There's a play again, but we don't know whether it's in the first or second index in the list
        if firstReturn:
            if card.abilities[0] == PLAY_AGAIN:
                return [firstReturn,card.abilities[1]]
            else:
                return [firstReturn,card.abilities[0]]

        # No play again ability, therefore the ability, if any, should be in the first index.
        else:
            return [firstReturn,card.abilities[0]]


    def runAbility(self, ability: int):
        """
        Will probably be done in SpendorDuel or SDGameHandler.
        It'll stay here for now until as a basis for the future implementation.
        """
        #TODO: write the code in the right file (see above)
        pass

        # match ability:
        #     #0 i.e. nothing:
        #     case 0:
        #         #skip everything, don't even bother looking at the second index
        #         pass
        #     #Choose token:
        #     case CHOOSE_GEMSTONE:
        #         #we'll pop the JewelCard instance, change it, then add it to the inventory
        #     #Play again:
        #     case PLAY_AGAIN:
        #         #just call the play method/return the play code or smth, idk
        #     #Take a token:
        #     case TAKE_A_TOKEN:
        #         #something similar to SDGameHandler.tokenCapture()
        #     #Get a privilege:
        #     case GET_PRIVILEGE:
        #         #call the method, I believe the get a privilege stuff works the same regardless of the way you get one
        #     #steal token:
        #     case STEAL_GEMSTONE
        #         #check the opponents inventory, if the chosen token is there we subtract it, if not there'll be an error

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