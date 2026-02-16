from dataclasses import dataclass, field
from typing import Optional, List

from .Constants import *
from .utils import leftPadding


@dataclass
class Card:
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

    def draw(self, emoji: bool = True) -> List[str]:
        """
        Retunrs a list of seven strings (one per lign) that represents the card.
        Will be used to display the card in the terminal.
        """
        # abilities
        strAbilities = leftPadding(" ".join(abilitiesEmoji[emoji].get(a, "") for a in self.abilities), 7)

        # Prestige points
        if not self.nbPrestige:
            strPrestige = "   "
        else:
            strPrestige = Fore.WHITE+Style.BRIGHT + leftPadding(f"{PrestigeEmoji[emoji]}{self.nbPrestige}", 3) + Fore.RESET+Style.NORMAL

        # Crown points
        if not self.nbCrowns:
            strCrowns = "   "
        else:
           strCrowns = Fore.YELLOW+Style.BRIGHT + leftPadding(f"{CrownEmoji[emoji]}{self.nbCrowns}", 3) + Fore.RESET+Style.NORMAL

        # jewel
        if not self.nbJewel:
            strJewel = "   "
        else:
            strJewel = tokenColors[self.tokenType] \
                   + leftPadding(f"{jewelEmojis[emoji][self.tokenType]}{self.nbJewel}", 3) \
                   + tokenColors[None]

        # Required tokens display
        strsTokens = []
        for token, nb in self.requirements.items():
            if nb:
                strsTokens.append(tokenColors[token]
                                  + leftPadding(f"{tokenEmojis[emoji][token]}{nb}", 3)
                                  + tokenColors[None])
            else:
                strsTokens.append("   ")

        #royal card
        if self.isRoyal():
            strCrowns = Fore.YELLOW+Style.BRIGHT \
                + leftPadding(f"{RoyalEmoji[emoji]}", 5) \
                + Fore.RESET+Style.NORMAL
            strJewel = " "

        cardStrList = [
            f"┌───────────┐",
            f"│{strPrestige} {strCrowns} {strJewel}│",
            f"│{strsTokens[3]}        │",
            f"│{strsTokens[2]}        │",
            f"│{strsTokens[1]} {strAbilities}│",
            f"│{strsTokens[0]}        │",
            f"└───────────┘"
        ]

        return cardStrList

    def isRoyal(self) -> bool:
        """returns True if the card is a Royal Card, False otherwise"""
        return self.nbJewel == 0 and self.nbCrowns == 0 and self.requirements == {1: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}


    def __post_init__(self):
        # Token handling
        if not (isinstance(self.tokenType, int) or self.tokenType is None):
            try:
                self.tokenType = tokenTypesDict[self.tokenType]
            except KeyError:
                print("ERROR: Invalid tokenType. Check data.json or JewelCard instance")

        # Abilities handling
        translated_abilities = list()
        for ability in self.abilities:
            # using .Constants' "abilities" list
            if isinstance(ability, int) and 0 < ability < 6:
                translated_abilities.append(ability)
            else:
                try:
                    translated_abilities.append(abilitiesDictionary.get(ability))
                except ValueError:
                    print(f"ERROR: Ability '{ability}' unknown!")

        # only two abilities allowed
        translated_abilities.extend([0, 0])
        self.abilities = translated_abilities[:2]

        #translate a requirement list in dict
        if isinstance(self.requirements, list):
            if len(self.requirements) != 6:
                print("ERROR: requirement list is incorrect!")
            else:
                self.requirements = dict(zip([PEARL, BLUE_SAPPHIRE, DIAMOND, EMERALD, RUBY, OBSIDIAN], self.requirements))
