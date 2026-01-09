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

from colorama import Fore, Back, Style


# 2 pearls, 3 gold, 4 for each gemstone.
# Pearl, Gold, Blue Sapphire, Diamond (clear),	(Names I've chosen, no clue whether
# Emerald (green), Ruby (red), Obsidian (black)	there's official color names...)

# Represents the different tokens
tokenTypes = [
    "None",             # Not sure yet if it's useful
    "Pearl",            # Pearl token
    "Gold",             # Gold token
    "Blue Sapphire",    # Blue gemstone token
    "Diamond",          # Clear gemstone token
    "Emerald",          # Green gemstone token
    "Ruby",             # Red gemstone token
    "Obsidian",         # Black gemstone token
    "Any"               # Not really relevant for tokens. Used for jewel cards.
                        # really needed though? not sure.
]


NONE = None
PEARL = 1
GOLD = 2
BLUE_SAPPHIRE = 3
DIAMOND = 4
EMERALD = 5
RUBY = 6
OBSIDIAN = 7

tokenTypesDict = {
    "None":    None,
    "Pearl":    PEARL,
    "Gold":    GOLD,
    "Blue Sapphire":    BLUE_SAPPHIRE,
    "Diamond":    DIAMOND,
    "Emerald":    EMERALD,
    "Ruby":    RUBY,
    "Obsidian":    OBSIDIAN,
}

tokenTypesInt = [NONE, PEARL, GOLD, BLUE_SAPPHIRE, DIAMOND, EMERALD, RUBY, OBSIDIAN]

tokenColors = {
    None: Fore.RESET + Style.NORMAL + Back.RESET,
    PEARL: Fore.MAGENTA + Style.BRIGHT + Back.RESET,
    GOLD: Fore.YELLOW + Style.BRIGHT + Back.RESET,
    BLUE_SAPPHIRE: Fore.BLUE + Style.NORMAL + Back.RESET,
    DIAMOND: Fore.WHITE + Style.BRIGHT + Back.RESET,
    EMERALD: Fore.GREEN + Style.NORMAL + Back.RESET,
    RUBY: Fore.RED + Style.NORMAL + Back.RESET,
    OBSIDIAN: Fore.WHITE + Style.DIM + Back.RESET
}

tokenEmojis = {
    True: {
        None: "🃏",
        PEARL: "🟣",
        GOLD: "🟡",
        BLUE_SAPPHIRE: "🔵",
        DIAMOND: "⚪",
        EMERALD: "🟢",
        RUBY: "🔴",
        OBSIDIAN: "⚫"
},
    False: {c: tokenColors[c] + name[0] for name, c in tokenTypesDict.items()}
}

jewelEmojis = {
    True: {
            None: "🃏",
            PEARL: "🟪",
            GOLD: "🟨",
            BLUE_SAPPHIRE: "🟦",
            DIAMOND: "⬜",
            EMERALD: "🟩",
            RUBY: "🟥",
            OBSIDIAN: "⬛"
},
    False: {c: "G" + name[0] for name, c in tokenTypesDict.items()}
}


tokenEmojis = {
    True: {
        None: "🃏",
        PEARL: "🟣",
        GOLD: "🟡",
        BLUE_SAPPHIRE: "🔵",
        DIAMOND: "⚪",
        EMERALD: "🟢",
        RUBY: "🔴",
        OBSIDIAN: "⚫"
},
    False: {c: " " + name[0] for name, c in tokenTypesDict.items()}
}


# Abilities
PLAY_AGAIN = 1
CHOOSE_GEMSTONE = 2
TAKE_A_TOKEN = 3
GET_PRIVILEGE = 4
STEAL_GEMSTONE = 5


abilitiesDictionary = {
    "PlayAgain":   PLAY_AGAIN,     #🔄
    "ChooseGemstone":   CHOOSE_GEMSTONE,#💎
    "TakeAToken":   TAKE_A_TOKEN,   #🪙
    "GetAPrivilegeScroll":   GET_PRIVILEGE,  #🗞️
    "StealGemstonePearl":   STEAL_GEMSTONE  #🫳
}

abilitiesEmoji = {
    True: {
    PLAY_AGAIN: "🔄",
    CHOOSE_GEMSTONE: "💎",
    TAKE_A_TOKEN: "🪙",
    GET_PRIVILEGE: "🗞️",
    STEAL_GEMSTONE: "🫳"
},
    False: {
        PLAY_AGAIN: "PA",
        CHOOSE_GEMSTONE: "CG",
        TAKE_A_TOKEN: "TT",
        GET_PRIVILEGE: "GP️",
        STEAL_GEMSTONE: "SG"
    }
}

PrestigeEmoji = {True: "✨", False: "PP"}
CrownEmoji = {True: "👑", False: "CR"}
RoyalEmoji = {True: "🤴", False: "ROYAL"}
# # Items
# items = ["Token",
#          "Jewel Card",
#          "Booked Card",
#          "Royal Card",
#          "Privilege"
# ]

# TOKEN = 0
# JEWEL_CARD = 1
# BOOKED_CARD = 2
# ROYAL_CARD = 3
# PRIVILEGE = 4
#
# itemsDictionary = {
#     items[0] : TOKEN,
#     items[1] : JEWEL_CARD,
#     items[2] : BOOKED_CARD,
#     items[3] : ROYAL_CARD,
#     items[4] : PRIVILEGE
# }
#
# itemsEmoji = {
#     items[0] : "🪙",
#     items[1] : "💎",
#     items[2] : "🎟️",
#     items[3] : "👑",
#     items[4] : "🗞️",
# }


