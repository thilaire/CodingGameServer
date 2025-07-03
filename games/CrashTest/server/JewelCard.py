from dataclasses import dataclass, field
from typing import Optional

from .Constants import *

@dataclass
class JewelCard:
    """Base class for Jewel Cards. Each jewel card will be an instance of this class."""
    tokenType   : int|None  # see Constants.py
    nbJewel     : int       # 0,1,2
    nbPrestige  : int       # 0,1,2,5,6
    nbCrowns    : int       # 0,1,2,3
    abilities   : list[int] = field(default_factory = lambda : [0,0])
    requirements: dict = field(default_factory = lambda : {     #Required gemstones/jewels to buy this instance of JewelCard
        PEARL           :   0,  # PEARL,
        BLUE_SAPPHIRE   :   0,  # SAPPHIRE,
        DIAMOND         :   0,  # DIAMOND,
        EMERALD         :   0,  # EMERALD,
        RUBY            :   0,  # RUBY,
        OBSIDIAN        :   0   # OBSIDIAN
    })
    _comment: Optional[str] = None


    def __post_init__(self):
        # Allow ourselves to not only use (ints | None) for tokenType (though it's what's inside JewelCard), but
        # to also use names of the gemstones (in strings, which are all in tokenTypes & tokenTypesDict).
        if not (isinstance(self.tokenType, int) or self.tokenType is None):
            try:
                self.tokenType = tokenTypesDict[self.tokenType]
            except KeyError:
                print("ERROR: Invalid tokenType. Check data.json or JewelCard instance")

        # Abilities stuff
        if not (isinstance(self.abilities, list)):
            print("ERROR: Invalid abilities. Check data.json or JewelCard instance")
        else:

            # "translate" strs to ints
            for x in self.abilities:
                for i in range(5):
                    if x == abilities[i]:
                        x = i + 1
                        #what on earth did i want to do w/ the next line
                        # self.abilities[i] = i + 1
                #0 if not good
                if not ( isinstance(x, int) or not (0 < x < 6) ):
                    print(f"ERROR: ability {x} is unknown. Check data.json or JewelCard instance")


            # Only two ints in abilities. We just take the two first, or replace them with zeros.
            self.abilities.extend([0, 0])
            self.abilities = self.abilities[:2]

