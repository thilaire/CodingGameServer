"""
* --------------------- *
|                       |
|   Coding Game Server  |
|                       |
* --------------------- *

Authors: B. Lamon, based on T. Hilaire & J. Brajard's template file.
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
    "None"              # Not sure yet if it's useful
    "Pearl",            # Pearl token
    "Gold",             # Gold token
    "Blue Sapphire",    # Blue gemstone token
    "Diamond",          # Clear gemstone token
    "Emerald",          # Green gemstone token
    "Ruby",             # Red gemstone token
    "Obsidian"          # Black gemstone token
]
# I should've probably enumerated them and given them int numbers...
# would've been like this:  PEARL = 0
#                           GOLD = 1
#                           BLUE_SAPPHIRE = 2
#                           ...
# ehhh i'll do this

NONE = 0
PEARL = 1
GOLD = 2
BLUE_SAPPHIRE = 3
DIAMOND = 4
EMERALD = 5
RUBY = 6
OBSIDIAN = 7


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
    token: ( 0 if token == "None"
            else 2 if token == "Pearl"       # 2 pearls
            else 3 if token == "Gold"   # 3 gold tokens
            else 4)                     # 4 gemstone tokens
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