from dataclasses import dataclass, field
from typing import Optional

from .Constants import *

@dataclass
class RoyalCard:
    """Base class for Crown Cards."""
    nbPrestige  : int       # 0,1,2,5,6
    abilities   : list[int] = field(default_factory = lambda : [0,0])
    _comment: Optional[str] = None


    def __post_init__(self):
        # Abilities stuff
        if not (isinstance(self.abilities, list)):
            print("ERROR: Invalid abilities. Check data.json or CrownCard instance")
        else:

            # "translate" strs to ints
            for x in self.abilities:
                for i in range(5):
                    if x == abilities[i]:
                        x = i + 1
                        self.abilities[i] = i + 1
                #0 if not good
                if not ( isinstance(x, int) or not (0 < x < 6) ):
                    print(f"ERROR: ability {x} is unknown. Check data.json or CrownCard instance")


            # Only two ints in abilities. We just take the two first, or replace them with zeros.
            self.abilities.extend([0, 0])
            self.abilities = self.abilities[:2]

