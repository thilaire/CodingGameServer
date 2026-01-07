from dataclasses import dataclass, field
from typing import Optional, List

from .Constants import *


@dataclass
class JewelCard:
    """Base class for Jewel Cards. Each jewel card will be an instance of this class."""
    tokenType: int|None  # see Constants.py
    nbJewel: int       # 0,1,2
    nbPrestige: int       # 0,1,2,5,6
    nbCrowns: int       # 0,1,2,3
    abilities: list[int] = field(default_factory=lambda: [])
    requirements: dict = field(default_factory=lambda: {     # Required gemstones/jewels to buy this instance of JewelCard
        PEARL: 0, BLUE_SAPPHIRE: 0, DIAMOND: 0, EMERALD: 0, RUBY: 0, OBSIDIAN: 0
    })
    _comment: Optional[str] = None

    def cardDraw(self, emoji: bool = True) -> List[str]:
        """
        Retunrs a list of seven strings (one per lign) that represents the card.
        Will be used to display the card in the terminal.
        """
        # abilities
        strsAbilities = abilitiesEmoji.get(self.abilities[0], "  ") + abilitiesEmoji.get(self.abilities[1], "  ")
        # Prestige points
        if not self.nbPrestige:
            strPrestige = "   "
        elif emoji:
            strPrestige = f"✨{self.nbPrestige}"
        else:
            strPrestige = f"{Fore.WHITE}{Style.BRIGHT}PP{self.nbPrestige}{Fore.RESET}{Style.NORMAL}"
        # Crown points
        if not self.nbCrowns:
            strCrowns = "   "
        elif emoji:
            strCrowns = f"👑{self.nbCrowns}"
        else:
            strCrowns = f"{Fore.YELLOW}{Style.BRIGHT}CR{self.nbCrowns}{Fore.RESET}{Style.NORMAL}"
        # jewel
        if not self.nbJewel:
            strJewel = "   "
        elif emoji:
            strJewel = f"{tokenEmojis[1][self.tokenType]}{self.nbJewel}"
        else:
            strJewel = f"{tokenColors[self.tokenType]}G{tokenTypes[self.tokenType][0]}{self.nbJewel}{tokenColors[None]}"


        # Required tokens display
        strsTokens = []
        for key in self.requirements:
            if self.requirements[key]:
                if emoji:
                    strsTokens.append(f"{tokenEmojis[0][key]}{self.requirements[key]}")
                else:
                    strsTokens.append(f"{tokenColors[key]}{tokenTypes[key][0]}{self.requirements[key]}{tokenColors[None]} ")
        strsTokens.extend(["   ", "   ", "   ", "   "])

        cardStrList = [
            f"┌───────────┐",
            f"│{strPrestige} {strCrowns} {strJewel}│",
            f"│{strsTokens[3]}        │",
            f"│{strsTokens[2]}        │",
            f"│{strsTokens[1]}    {strsAbilities}│",
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

        #translate a requirement list in dict (didn't quite get the requirements right in the JSON file...)
        if isinstance(self.requirements, list):
            if len(self.requirements) != 6:
                print("ERROR: requirement list is incorrect!")
            else:
                self.requirements = dict(zip([PEARL, BLUE_SAPPHIRE, DIAMOND, EMERALD, RUBY, OBSIDIAN], self.requirements))
