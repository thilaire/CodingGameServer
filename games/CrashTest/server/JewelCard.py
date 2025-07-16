from dataclasses import dataclass, field
from typing import Optional, List

from .Constants import *

@dataclass
class JewelCard:
    """Base class for Jewel Cards. Each jewel card will be an instance of this class."""
    tokenType   : int|None  # see Constants.py
    nbJewel     : int       # 0,1,2
    nbPrestige  : int       # 0,1,2,5,6
    nbCrowns    : int       # 0,1,2,3
    abilities   : list[int] | list[str] = field(default_factory = lambda : [0,0])
    requirements: dict = field(default_factory = lambda : {     #Required gemstones/jewels to buy this instance of JewelCard
        PEARL           :   0,  # PEARL,
        BLUE_SAPPHIRE   :   0,  # SAPPHIRE,
        DIAMOND         :   0,  # DIAMOND,
        EMERALD         :   0,  # EMERALD,
        RUBY            :   0,  # RUBY,
        OBSIDIAN        :   0   # OBSIDIAN
    })
    _comment: Optional[str] = None

    def cardDraw(self) -> List[str]:
        """
        Retunrs a list of seven strings (one per lign) that represents the card.
        Will be used to display the card in the terminal.
        """
        strsAbilities = []
        # Ability display
        match self.abilities[0]:
            case 0:
                # nothing
                strsAbilities = ["  ", "  "]
            case 1:
                # play again
                strsAbilities = ["❗", "🔄"]
            case 2:
                # choose gemstone
                strsAbilities = ["❗", "💎"]
            case 3:
                # take token
                strsAbilities = ["❗", "🪙"]
            case 4:
                # privilege
                strsAbilities = ["❗", "🗞️"]
            case 5:
                # steal gemstone
                strsAbilities = ["❗", "🫳"]

        match self.abilities[1]:
            case 0:
                strsAbilities[1] = f" {strsAbilities[1]} "
            case 1:
                strsAbilities[1] = f"{strsAbilities[1]}🔄"
            case 2:
                strsAbilities[1] = f"{strsAbilities[1]}💎"
            case 3:
                strsAbilities[1] = f"{strsAbilities[1]}🪙"
            case 4:
                strsAbilities[1] = f"{strsAbilities[1]}🗞️"
            case 5:
                strsAbilities[1] = f"{strsAbilities[1]}🫳"

        # Requirements at the top of the card
        strsTop = []
        if self.nbPrestige:
            strsTop.append(f"✨{self.nbPrestige}")
        else:
            strsTop.append("   ")

        if self.nbCrowns:
            strsTop.append(f"👑{self.nbCrowns}")
        else:
            strsTop.append("   ")

        if self.nbJewel:
            strsTop.append(f"{tokenEmojis[0][self.tokenType]}{self.nbJewel}")
        else:
            strsTop.append("   ")

        # Required tokens display
        strsTokens = ["   ", "   ", "   ", "   "]
        i = 0
        for key in self.requirements:
            if self.requirements[key]:
                strsTokens[i] = f"{tokenEmojis[0][key]}{self.requirements[key]}"
                i += 1

        cardStrList = [
            f"┌───────────┐",
            f"│{strsTop[0]} {strsTop[1]} {strsTop[2]}│",
            f"│{strsTokens[3]}        │",
            f"│{strsTokens[2]}     {strsAbilities[0]} │",
            f"│{strsTokens[1]}    {strsAbilities[1]}│",
            f"│{strsTokens[0]}        │",
            f"└───────────┘"
        ]

        return cardStrList


    def __post_init__(self):
        # Allow ourselves to not only use (ints | None) for tokenType (though it's what's inside JewelCard), but
        # to also use names of the gemstones (in strings, which are all in tokenTypes & tokenTypesDict).
        if not (isinstance(self.tokenType, int) or self.tokenType is None):
            try:
                self.tokenType = tokenTypesDict[self.tokenType]
            except KeyError:
                print("ERROR: Invalid tokenType. Check data.json or JewelCard instance")

        # Abilities handling
        translated_abilities = list()
        for ability in self.abilities:
            # using .Constants' "abilities" list
            if isinstance(ability, str):
                if ability in abilities:
                    try:
                        translated_abilities.append(abilities.index(ability) + 1) # L. 113 in Constants (indexed from 1)
                    except ValueError:
                        print(f"ERROR: Ability '{ability}' unknown!")
                else:
                    translated_abilities.append(0)
            elif isinstance(ability, int) and 0 < ability < 6:
                translated_abilities.append(ability)
            else:
                print(f"ERROR: Ability '{ability}' unknown!")
                translated_abilities.append(0)

        translated_abilities.extend([0, 0])
        self.abilities = translated_abilities[:2]

        #translate requirement list in dict (didn't quite get the requirements right in the JSON file...)
        if isinstance(self.requirements, list):
            if len(self.requirements) != 6:
                print("ERROR: requirement list is incorrect!")
            else:
                self.requirements = dict(zip([PEARL, BLUE_SAPPHIRE, DIAMOND, EMERALD, RUBY, OBSIDIAN], self.requirements))
