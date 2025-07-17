from dataclasses import dataclass, field
from selectors import SelectSelector
from typing import List

from .Constants import *
from .JewelCard import JewelCard
from .RoyalCard import RoyalCard

@dataclass
class Inventory:
    _nbPrivileges   : int = 0
    tokens          : list[int|None] = field(default_factory = lambda :
        [None, 0, 0, 0, 0, 0, 0, 0])
    jewelCards      : dict = field(default_factory = lambda :{
        None            : [], #list[JewelCard],
        BLUE_SAPPHIRE   : [], #list[JewelCard],
        DIAMOND         : [], #list[JewelCard],
        EMERALD         : [], #list[JewelCard],
        RUBY            : [], #list[JewelCard],
        OBSIDIAN        : []  #list[JewelCard]
    })
    bookedCards     : list[JewelCard] = field(default_factory = lambda: []) #three booked cards at most
    royalCards      : list[RoyalCard] = field(default_factory = lambda: [])
    thresholds      : list[bool] = field(init = False) # for the crown cards [True, False] when reaching 3 crowns, [True, True] when reaching 6

    def __post_init__(self):
        self.thresholds = [False, False]


    #Getters & whatnot
    def nbPrestige(self, _type: int|None) -> int:
        """
        Returns the amount of prestige points.
        To get all the prestige points (including the ones from royal cards), _type should be -1.
        """
        #run through all the jewelCards colors;
        #run through all the cards;
        #sum up all the prestige points

        if _type == -1:
            return sum(card.nbPrestige for colorList in self.jewelCards.values() for card in colorList) + sum(card.nbPrestige for card in self.royalCards)
        else:
            try:
                return sum(card.nbPrestige for card in self.jewelCards[_type])
            except KeyError:
                print(f"ERROR: No such Jewel Card type ({_type}) exists!")
                return -1

    def nbCrowns(self) -> int:
        """
        Returns the total amount of crowns in the inventory.
        """
        return sum(card.nbCrowns for color in self.jewelCards.values() for card in color)

    @property
    def nbPrivileges(self) -> int:
        """
        returns the amount of privileges
        """
        return self._nbPrivileges

    def nbJewelCards(self, _type: int|None) -> int:
        """
        Returns the number of jewels of a specified type.
        """
        #go through all the cards, select every _type card, sum them.
        if _type is None:
            #should be 0 caus there is no such thing as a None jewel
            return sum(card.nbJewel for color in self.jewelCards.values() for card in color if card.tokenType is None)
        else:
            return sum(card.nbJewel for color in self.jewelCards.values() for card in color if card.tokenType == _type)

    def nbTokens(self, _type: int) -> int:
        """
        Returns the amount of tokens of a specified type.
        """
        return self.tokens[_type]

    def nbRoyalCards(self) -> int:
        return len(self.royalCards)



    #Setters & similar methods
    
    @nbPrivileges.setter
    def nbPrivileges(self, val) -> None:
        self._nbPrivileges = val

    def addJewelCard(self, jewelCard) -> None:
        """
        pops jewelCardsList[index] to add it to the inventory.
        jewelCardsList is either the level 1, 2  or 3 deck.
        """
        self.jewelCards[jewelCard.tokenType].append(jewelCard)

    def chooseRoyalCard(self, card: RoyalCard) -> None:
        """
        Choosing a Royal Card requires a player to pass either 3 or 6 crowns.
        (Checking when someone passes 3 or 6 crowns will be done somewhere else?)
        """
        if self.nbCrowns() >= 3 and self.thresholds[0] == False:
            self.thresholds[0] = True
            self.royalCards.append(card)
        elif self.nbCrowns() >= 6 and self.thresholds[1] == False:
            self.thresholds[1] = True
            self.royalCards.append(card)
        else:
            print(f"ERROR: shouldn't choose a royal card! ({self.nbCrowns()} crowns)")

    def buyJewelCard(self, card: JewelCard) -> List[bool|int]:
        """
        Just checks whether we can add the card to the inventory.
        Returns a list in the following format: [playAgain: bool ; specialMove: int]
        playAgain   : whether we're playing again or not
        specialAbility : which one of the 5, if any. 0 if no special ability, -1 if acquiring failed (which case, error).

        (We'll handle the card special ability in either SDGameHandler or SplendorDuel, not sure yet.)
        """
        # if you're trying to understand the code, good luck because I don't despite the comments 👍

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

                        # which case we add the negative number to the gold tokens, then put it to zero,
                        # then check whether there's anything < 0 in the tokens ?
                        self.tokens[GOLD] += self.tokens[reqJewel]
                        self.tokens[reqJewel] = 0
                #in the other case, we just subtract the amount of tokens needed to purchase the card
                else:
                    self.tokens[reqJewel] -= card.requirements[reqJewel] - dictSum[reqJewel]
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


    def chooseGemstone(self):
        #should it be in SDGameHandler?
        pass

    def addToken(self, idToken, amount) -> None:
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

    def canBookACard(self) -> int:
        """
        Checks whether it's possible for this player's inventory to book a certain card.
        """
        # The following was written in `SplendorDuel.py`:
        #
        #		-Book a Jewel card (the opponent isn't supposed to see it anymore,
        #		though they can memorize it (not really relevant to this computer version))
        #			conditions:	-You either take one from the pyramid or one from the three stacks (level 1, 2 or 3)
        #						-You have to take a gold token from the board.
        #						-Illegal if there isn't one anymore
                                    #   -> Not handled here I guess?
        #						-Illegal if you already have three booked cards
        #						-You do not need to buy any of the cards you booked
        #
        
        if len(self.bookedCards) >= 3:
            print(f"ERROR: you already have {len(self.bookedCards)} booked cards! (3 at most)")
            return -1
        else:
            return 0

    def bookCard(self, card: JewelCard) -> int:
        if self.canBookACard() == -1:
            return -1
        else:
            self.bookedCards.append(card)
            return 0
        