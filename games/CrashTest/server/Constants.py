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

NONE            =   None
PEARL           =   1
GOLD            =   2
BLUE_SAPPHIRE   =   3
DIAMOND         =   4
EMERALD         =   5
RUBY            =   6
OBSIDIAN        =   7

tokenTypesDict = {
    "None"          :    None,
    "Pearl"         :    PEARL,
    "Gold"          :    GOLD,
    "Blue Sapphire" :    BLUE_SAPPHIRE,
    "Diamond"       :    DIAMOND,
    "Emerald"       :    EMERALD,
    "Ruby"          :    RUBY,
    "Obsidian"      :    OBSIDIAN,
}

tokenTypesInt = [NONE,PEARL,GOLD,BLUE_SAPPHIRE,DIAMOND,EMERALD,RUBY,OBSIDIAN]


tokenColors = [
    Fore.RESET      + Style.NORMAL  + Back.RESET,   # NONE
    Fore.MAGENTA    + Style.BRIGHT  + Back.RESET,   # PEARL
    Fore.YELLOW     + Style.BRIGHT  + Back.RESET,   # GOLD
    Fore.BLUE       + Style.NORMAL  + Back.RESET,   # SAPPHIRE
    Fore.WHITE      + Style.BRIGHT  + Back.RESET,   # DIAMOND
    Fore.GREEN      + Style.NORMAL  + Back.RESET,   # EMERALD
    Fore.RED        + Style.NORMAL  + Back.RESET,   # RUBY
    Fore.WHITE      + Style.DIM     + Back.RESET    # OBSIDIAN
]

tokenEmojis = [{
    None            : "🃏",
    PEARL           : "🟣",
    GOLD            : "🟡",
    BLUE_SAPPHIRE   : "🔵",
    DIAMOND         : "⚪",
    EMERALD         : "🟢",
    RUBY            : "🔴",
    OBSIDIAN        : "⚫"
},
    {
        None            : "🃏",
        PEARL           : "🟪",
        GOLD            : "🟨",
        BLUE_SAPPHIRE   : "🟦",
        DIAMOND         : "⬜",
        EMERALD         : "🟩",
        RUBY            : "🟥",
        OBSIDIAN        : "⬛"
    },
    {
        None            : f"{tokenColors[0]}N",
        PEARL           : f"{tokenColors[1]}{tokenTypes[1][0]}",
        GOLD            : f"{tokenColors[2]}{tokenTypes[2][0]}",
        BLUE_SAPPHIRE   : f"{tokenColors[3]}{tokenTypes[3][0]}",
        DIAMOND         : f"{tokenColors[4]}{tokenTypes[4][0]}",
        EMERALD         : f"{tokenColors[5]}{tokenTypes[5][0]}",
        RUBY            : f"{tokenColors[6]}{tokenTypes[6][0]}",
        OBSIDIAN        : f"{tokenColors[7]}{tokenTypes[7][0]}"
    }
]

#Probably useless since we'll manage the game with a sort of bank... we'll see.
    # Maximum token amounts. They're the ones we're going to display on the board.
    # (side note: how are we going to display that on a console screen?)
maxTokenAmounts = {
    token: (  None if token == "None"
            else 2 if token == "Pearl"       # 2 pearls
            else 3 if token == "Gold"   # 3 gold tokens
            else 4)                     # 4 gemstone tokens
            for i,token in enumerate(tokenTypes)
}


# Abilities
abilities = ["PlayAgain",
             "ChooseGemstone",      # Need to own the gemstone card first, otherwise they can't buy a card w/ this ability
             "TakeAToken",          # On the board
             "GetAPrivilegeScroll", # If none available, steal from the opponent
             "StealGemstonePearl"]  # steal a gemstone or a pearl token from the opponent. NOT GOLD TOKEN

PLAY_AGAIN      =   1
CHOOSE_GEMSTONE =   2
TAKE_A_TOKEN    =   3
GET_PRIVILEGE   =   4
STEAL_GEMSTONE  =   5

abilitiesDictionary = {
    abilities[0]:   PLAY_AGAIN,     #🔄
    abilities[1]:   CHOOSE_GEMSTONE,#💎
    abilities[2]:   TAKE_A_TOKEN,   #🪙
    abilities[3]:   GET_PRIVILEGE,  #🗞️
    abilities[4]:   STEAL_GEMSTONE  #🫳
}

# Items
items = ["Token",
         "Jewel Card",
         "Booked Card",
         "Royal Card",
         "Privilege"
        ]

TOKEN = 0
JEWEL_CARD = 1
BOOKED_CARD = 2
ROYAL_CARD = 3
PRIVILEGE = 4

itemsDictionary = {
    items[0] : TOKEN,
    items[1] : JEWEL_CARD,
    items[2] : BOOKED_CARD,
    items[3] : ROYAL_CARD,
    items[4] : PRIVILEGE
}

#hopefully won't be useless
itemsEmoji = {
    items[0] : "🪙",
    items[1] : "💎",
    items[2] : "🎟️",
    items[3] : "👑",
    items[4] : "🗞️",
}