"""
* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: B. Lamon, based on T. Hilaire & J. Bajard's template file.
Licence: GPL

File: Constants.py
	Contains the constants of the game
	->	Defines the values of the cards, number of a specific token,

Copyright 2025 B. Lamon
"""

# 2 pearls, 3 gold, 4 for each gemstone.
# Pearl, Gold, Blue Sapphire, Diamond (clear),	(Names I've chosen, no clue whether
# Emerald (green), Ruby (red), Obsidian (black)	there's official color names...)

# Represents the different tokens
tokenTypes = [
    "Pearl",            # Pearl token
    "Gold",             # Gold token
    "Blue Sapphire",    # Blue gemstone token
    "Diamond",          # Clear gemstone token
    "Emerald",          # Green gemstone token
    "Ruby",             # Red gemstone token
    "Obsidian"          # Black gemstone token
]

tokenAmounts = dict()
"""
# ugly but works
for element in tokenTypes:
    if element == "Pearl":
        tokenAmounts["Pearl"] = 2
    elif element == "Gold":
        tokenAmounts["Gold"] = 3
    else:
        tokenAmounts[element] = 4
"""
# pretty (dictionary comprehension, but with a weird synthax caus I can read it better)
tokenAmounts = {
    token: (2 if i == 0         # 2 pearls
            else 3 if i == 1    # 3 gold tokens
            else 4)             # 4 gemstone tokens
            for i,token in enumerate(tokenTypes)
}

# Card decks
# TODO: list every card of the decks
lvl1JewelleryCards = list()
lvl2JewelleryCards = list()
lvl3JewelleryCards = list()
crownCards = list()

# Abilities ?
Abilities = ["PlayAgain",
             "ChooseGemstone",      # Need to own the gemstone card first, otherwise they can't buy a card w/ this ability
             "TakeAToken",          # On the board
             "GetABenefit",         # If none available, steal from the opponent
             "TakeGemstonePearl"]   # steal a gemstone or a pearl token from the opponent. NOT GOLD TOKEN


# inventories ?

#