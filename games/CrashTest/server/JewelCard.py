from dataclasses import dataclass, field
from .Constants import *

@dataclass
class JewelCard:
    """Base class for Jewel Cards. Each jewel card will be an instance of this class."""
    tokenType: int|None # see Constants.py
    nbJewel: int        # 0,1,2
    nbPrestige: int     # 0,1,2,5,6
    nbCrowns: int       # 0,1,2,3
    abilities: list[str] = field(default_factory = lambda : ["None"])    # maybe a list of strings would be better?
                                                                        # Probably, there's an instance of a card w/ two abilities...
    requirements: dict = field(default_factory = lambda : {     #Needed to buy said JewelCard
        PEARL: 0, #PEARL
        tokenTypes[3]: 0, #SAPPHIRE
        tokenTypes[4]: 0, #DIAMOND,
        tokenTypes[5]: 0, #EMERALD,
        tokenTypes[6]: 0, #RUBY,
        tokenTypes[7]: 0  #OBSIDIAN
    })


    def __post_init__(self):
        #
        if not (isinstance(self.tokenType, int) or self.tokenType is None):
            try:
                self.tokenType = tokenTypesDict[self.tokenType]
            except KeyError:
                print("Invalid tokenType !!")

