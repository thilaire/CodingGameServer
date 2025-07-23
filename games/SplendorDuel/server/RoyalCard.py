from dataclasses import dataclass, field
from typing import Optional, List

from .Constants import *
#TODO: make a "Card" class, that way RoyalCard & JewelCard would inherit from Card ?
@dataclass
class RoyalCard:
    """Base class for Crown Cards."""
    nbPrestige  : int       # 0,1,2,5,6
    abilities   : list[int] = field(default_factory = lambda : [0,0])
    _comment: Optional[str] = None

    def cardDraw(self, emoji: bool = True) -> List[str]:
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
                if emoji:
                    strsAbilities = ["❗", "🔄"]
                else:
                    strsAbilities = [f"{Fore.RED}{Style.BRIGHT}!!{Fore.RESET}{Style.NORMAL}", "PA"]
            case 2:
                # choose gemstone
                if emoji:
                    strsAbilities = ["❗", "💎"]
                else:
                    strsAbilities = [f"{Fore.RED}{Style.BRIGHT}!!{Fore.RESET}{Style.NORMAL}", "CG"]
            case 3:
                # take token
                if emoji:
                    strsAbilities = ["❗", "🪙"]
                else:
                    strsAbilities = [f"{Fore.RED}{Style.BRIGHT}!!{Fore.RESET}{Style.NORMAL}", "TT"]
            case 4:
                # privilege
                if emoji:
                    strsAbilities = ["❗", "🗞️"]
                else:
                    strsAbilities = [f"{Fore.RED}{Style.BRIGHT}!!{Fore.RESET}{Style.NORMAL}", "PS"]
            case 5:
                # steal token
                if emoji:
                    strsAbilities = ["❗", "🫳"]
                else:
                    strsAbilities = [f"{Fore.RED}{Style.BRIGHT}!!{Fore.RESET}{Style.NORMAL}", "ST"]

        match self.abilities[1]:
            case 0:
                strsAbilities[1] = f" {strsAbilities[1]} "
            case 1:
                if emoji:
                    strsAbilities[1] = f"{strsAbilities[1]}🔄"
                else:
                    strsAbilities[1] = f"{Fore.YELLOW}{strsAbilities[1]}{Fore.RED}PA{Fore.RESET}"
            case 2:
                if emoji:
                    strsAbilities[1] = f"{strsAbilities[1]}💎"
                else:
                    strsAbilities[1] = f"{Fore.YELLOW}{strsAbilities[1]}{Fore.RED}CG{Fore.RESET}"
            case 3:
                if emoji:
                    strsAbilities[1] = f"{strsAbilities[1]}🪙"
                else:
                    strsAbilities[1] = f"{Fore.YELLOW}{strsAbilities[1]}{Fore.RED}TT{Fore.RESET}"
            case 4:
                if emoji:
                    strsAbilities[1] = f"{strsAbilities[1]}🗞️"
                else:
                    strsAbilities[1] = f"{Fore.YELLOW}{strsAbilities[1]}{Fore.RED}PS{Fore.RESET}"
            case 5:
                if emoji:
                    strsAbilities[1] = f"{strsAbilities[1]}🫳"
                else:
                    strsAbilities[1] = f"{Fore.YELLOW}{strsAbilities[1]}{Fore.RED}ST{Fore.RESET}"

        # Requirements at the top of the card
        strsTop = []
        if self.nbPrestige:
            if emoji:
                strsTop.append(f"✨{self.nbPrestige}")
            else:
                strsTop.append(f"{Fore.WHITE}{Style.BRIGHT}PP{self.nbPrestige}{Fore.RESET}{Style.NORMAL}")
        else:
            strsTop.append("   ")

        if emoji:
            strsTop.append(f"{Fore.YELLOW}{Style.BRIGHT}👑ROYAL{Fore.RESET}{Style.NORMAL}")
        else:
            strsTop.append(f"{Fore.YELLOW}{Style.BRIGHT} ROYAL {Fore.RESET}{Style.NORMAL}")

        cardStrList = [
            f"┌───────────┐",
            f"│{strsTop[0]} {strsTop[1]}│",
            f"│           │",
            f"│        {strsAbilities[0]} │",
            f"│       {strsAbilities[1]}│",
            f"│           │",
            f"└───────────┘"
        ]

        return cardStrList

    def __post_init__(self):
        # Abilities stuff
        if not (isinstance(self.abilities, list)):
            print("ERROR: Invalid abilities. Check data.json or CrownCard instance")
        else:

            # Abilities handling
            translated_abilities = list()
            for ability in self.abilities:
                # using .Constants' "abilities" list
                if isinstance(ability, str):
                    if ability in abilities:
                        try:
                            translated_abilities.append(
                                abilities.index(ability) + 1)  # L. 113 in Constants (indexed from 1)
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

            # Only two ints in abilities. We just take the two first, or replace them with zeros.
            self.abilities.extend([0, 0])
            self.abilities = self.abilities[:2]

