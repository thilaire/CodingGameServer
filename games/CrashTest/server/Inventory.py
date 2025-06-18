from dataclasses import dataclass
from .Constants import * #really needed?
from .JewelCard import JewelCard

@dataclass
class Inventory:
    jewelCards: list[JewelCard]
    tokens: list[int]
    _nbPrivileges: int


    def nbCardJewels(self):
        """
        Returns the number of card jewels.
        It is overloaded (nbCardJewels() or nbCardJewels(_type)):
        either returns the overall number of card jewels, or only the number of a specified type.
        """
        #we should go through all the jewel cards, and sum all nbJewel
        return sum(x.nbJewel for x in self.jewelCards)

    #returns the number of jewels of a certain type
    def nbCardJewels(self, _type):
        """
        Returns the number of card jewels.
        It is overloaded (nbCardJewels() or nbCardJewels(_type)):
        either returns the overall number of card jewels, or only the number of a specified type.
        """
        #go through all the cards, select every _type card, sum them.
        return sum(self.jewelCards[_type].nbJewels) #WRONG, index _type will only give us one card, which may or may not be of the wanted _type.
                                                    #we should go into all the cards and sum them if and ONLY IF they are of the type.
                                                    #something like "sum(for x in self.jewelCards, if jewelCards.tokenType == _type)"
                                                    #but I don't know the synthax

    def nbTokens(self, _type):
        """
        returns the amount of tokens of a specified type.
        """

    def nbPrestige(self):
        """
        returns the amount of prestige points
        """

    @property
    def nbPrivileges(self):
        """
        returns the amount of privileges
        """
        return self._nbPrivileges

    @nbPrivileges.setter
    def nbPrivileges(self, val):
        self._nbPrivileges = val