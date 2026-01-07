import json


from .SDGameHandler import SDGameHandler
from .JewelCard import JewelCard
from .RoyalCard import RoyalCard
from .Inventory import Inventory
from .Constants import *

if __name__ == "__main__":
    # #-----------------------------------------------------------------------------------------------------------------
    #checking whether we can update the board ✅
    # #-----------------------------------------------------------------------------------------------------------------
    game = SDGameHandler()

    game.board[0][0] = PEARL
    game.board[4][4] = RUBY

    print(game.strBoard(True))







    # #-----------------------------------------------------------------------------------------------------------------
    # #add cards to inventory ✅
    # #-----------------------------------------------------------------------------------------------------------------

    # #tokenType, nbJewels, nbPrestige, nbCrowns
    # carte0 = JewelCard(BLUE_SAPPHIRE, 2, 2, 0, ["None"])
    # carte1 = JewelCard(RUBY, 2, 2, 2)
    # carte2 = JewelCard(RUBY, 2, 3, 1)
    # carte3 = JewelCard(RUBY,6,5,3)
    #
    # cards = [carte0,carte1,carte2,carte3]

    #probably need this later in some other file, mb even in this one
    gemCards = [NONE, BLUE_SAPPHIRE, DIAMOND, EMERALD, RUBY, OBSIDIAN]

    #dict init
    jewel_cards_dict = { gem: [] for gem in gemCards}

    # #auto fetch + add card to dict
    # for card in cards:
    #     jewel_cards_dict[card.tokenType].append(card)

    inv = Inventory(nbPrivileges= 0, jewelCards = jewel_cards_dict)

    #-------------------------------------------------------------------------------------------------------------------
    #check for errors ✅
    #-------------------------------------------------------------------------------------------------------------------
    # print(inv)
    # print()
    # inv.addToken(None, 3)
    # inv.addToken(1,3)
    # inv.addToken(2,4)
    # inv.addToken(3,5)
    # inv.addToken(4,4)
    # print()
    # print(inv)
    # print()

    #Parse JSON data✅
    # with open("cards/data.json", "r") as file:
    #     data = json.load(file)
    #
    # print("Level 1 :")
    # lvl1cards = [JewelCard(**card) for card in data["level1"]]
    # for x in lvl1cards:
    #     print(x)
    #
    # print()
    # print("Level 2: ")
    # lvl2cards = [JewelCard(**card) for card in data["level2"]]
    # for x in lvl2cards:
    #     print(x)
    #
    # print()
    # print("Level 3: ")
    # lvl3cards = [JewelCard(**card)for card in data["level3"]]
    # for x in lvl3cards:
    #     print(x)
    #
    # #could probably do a list of 3 lists of JCard instances, would've been prettier.
    #
    # print()
    # print("Inventory before adding lvl1cards[1]:")
    # print(inv.jewelCards)
    # inv.addJewelCard(lvl1cards, 1) #1 more prestige point
    # print("Inventory after")
    # print(inv.jewelCards)
    #
    # print(f"lvl1cards[1] : {lvl1cards[1]}")

    # #-----------------------------------------------------------------------------------------------------------------
    #checking for errors ✅
    # #-----------------------------------------------------------------------------------------------------------------
    # print(inv.nbPrestige(-1))
    # print(inv.nbPrestige(6))
    # print(inv.nbPrestige(9))

    # #-----------------------------------------------------------------------------------------------------------------
    # # checking inventory.addJewelCard() & ability translation
    # #-----------------------------------------------------------------------------------------------------------------
    print("Inventory before adding anything :")
    print(inv)
    inv.addJewelCard(JewelCard(tokenType = BLUE_SAPPHIRE, nbJewel= 1, nbCrowns=0,nbPrestige=0,abilities=["PlayAgain", "ChooseGemstone"]))
    print("Inventory after adding this jewel card:")
    print(inv)

    # #-----------------------------------------------------------------------------------------------------------------
    # # checking inventory.buyJewelCard()
    # #-----------------------------------------------------------------------------------------------------------------
    # # adding tokens
    # inv.addToken(GOLD, 1)
    # inv.addToken(BLUE_SAPPHIRE, 1)
    # inv.addToken(EMERALD,3)
    #
    # # card to purchase
    # toBuy = JewelCard(None, 0, 3, 2, [PLAY_AGAIN, CHOOSE_GEMSTONE], requirements={     #Required gemstones/jewels to buy this instance of JewelCard
    #     PEARL           :   1,  # PEARL,
    #     BLUE_SAPPHIRE   :   2,  # SAPPHIRE,
    #     DIAMOND         :   0,  # DIAMOND,
    #     EMERALD         :   3,  # EMERALD,
    #     RUBY            :   0,  # RUBY,
    #     OBSIDIAN        :   0   # OBSIDIAN
    # })
    #
    # print()
    # print('The following is "inv.buyJewelCard(toBuy)": ')
    # #further testing.
    # # -> Breakpoint/debug stuff,
    # #   ->see how many tokens there's left, could we have used less ? (nope) ✅
    # # -> test of different cases where it shouldn't work
    # #   -> not enough tokens ✅
    # #   -> not enough tokens but enough jewel cards ✅
    # #   -> not enough jewel cards but enough tokens ✅
    # #   -> not enough tokens nor jewel cards ✅
    # #   -> not enough tokens but enough gold ✅
    #
    # print(inv.buyJewelCard(toBuy))
    #
    # # #-----------------------------------------------------------------------------------------------------------------
    # # At this point, we have zero token in our inventory.
    # # Though we have one SAPPHIRE jewel card (w/ 1 gem)
    #
    # # card to purchase (NOT ENOUGH PEARL TOKEN) ✅
    # toBuy = JewelCard(None, 0, 3, 2, [PLAY_AGAIN, CHOOSE_GEMSTONE], requirements={     #Required gemstones/jewels to buy this instance of JewelCard
    #     PEARL           :   1,  # PEARL,
    #     BLUE_SAPPHIRE   :   1,  # SAPPHIRE,
    #     DIAMOND         :   0,  # DIAMOND,
    #     EMERALD         :   0,  # EMERALD,
    #     RUBY            :   0,  # RUBY,
    #     OBSIDIAN        :   0   # OBSIDIAN
    # })
    # print("Card to purchase without enough tokens:")
    # print(toBuy)
    # print('The following is "inv.buyJewelCard(toBuy)": ')
    # print(inv.buyJewelCard(toBuy))
    #
    # # #-----------------------------------------------------------------------------------------------------------------
    # # At this point, we have zero token in our inventory.
    # # Though we have one SAPPHIRE jewel card (w/ 1 gem)
    #
    # # card to purchase (NO TOKEN, JUST A JEWEL CARD) ✅
    # toBuy = JewelCard(None, 0, 3, 2, [PLAY_AGAIN, CHOOSE_GEMSTONE], requirements={     #Required gemstones/jewels to buy this instance of JewelCard
    #     PEARL           :   0,  # PEARL,
    #     BLUE_SAPPHIRE   :   1,  # SAPPHIRE,
    #     DIAMOND         :   0,  # DIAMOND,
    #     EMERALD         :   0,  # EMERALD,
    #     RUBY            :   0,  # RUBY,
    #     OBSIDIAN        :   0   # OBSIDIAN
    # })
    # print()
    # print("Card to purchase with just enough jewels (no token though):")
    # print(toBuy)
    # print('The following is "inv.buyJewelCard(toBuy)": ')
    # print(inv.buyJewelCard(toBuy))
    #
    # # #-----------------------------------------------------------------------------------------------------------------
    # # At this point, we have zero token in our inventory.
    # # Though we have one SAPPHIRE jewel card (w/ 1 gem)
    #
    # # card to purchase (not enough jewel cards but enough tokens)
    # toBuy = JewelCard(None, 0, 3, 2, [PLAY_AGAIN, CHOOSE_GEMSTONE], requirements={     #Required gemstones/jewels to buy this instance of JewelCard
    #     PEARL           :   2,  # PEARL,
    #     BLUE_SAPPHIRE   :   4,  # SAPPHIRE,
    #     DIAMOND         :   4,  # DIAMOND,
    #     EMERALD         :   4,  # EMERALD,
    #     RUBY            :   4,  # RUBY,
    #     OBSIDIAN        :   4   # OBSIDIAN
    # })
    # #max out inventory EXCEPT for sapphire
    # inv.addToken(PEARL, 2)
    # inv.addToken(BLUE_SAPPHIRE, 3)
    # inv.addToken(DIAMOND, 4)
    # inv.addToken(EMERALD, 4)
    # inv.addToken(RUBY, 4)
    # inv.addToken(OBSIDIAN, 4)
    #
    #
    # print()
    # print("Card to purchase with just enough jewels (no token though):")
    # print(toBuy)
    # print('The following is "inv.buyJewelCard(toBuy)": ')
    # print(inv.buyJewelCard(toBuy))
    # print(inv.tokens)
    # # works for now + we have no tokens in the inventory anymore
    #
    # # #-----------------------------------------------------------------------------------------------------------------
    # # At this point, we have zero token in our inventory.
    # # Though we have one SAPPHIRE jewel card (w/ 1 gem)
    #
    # # card to purchase (not enough tokens nor jewel cards) ✅
    # toBuy = JewelCard(None, 0, 3, 2, [PLAY_AGAIN, CHOOSE_GEMSTONE], requirements={     #Required gemstones/jewels to buy this instance of JewelCard
    #     PEARL           :   1,  # PEARL,
    #     BLUE_SAPPHIRE   :   2,  # SAPPHIRE,
    #     DIAMOND         :   0,  # DIAMOND,
    #     EMERALD         :   0,  # EMERALD,
    #     RUBY            :   0,  # RUBY,
    #     OBSIDIAN        :   0   # OBSIDIAN
    # })
    # print()
    # print("Card to purchase with just enough jewels (no token though):")
    # print(toBuy)
    # print('The following is "inv.buyJewelCard(toBuy)": ')
    # print(inv.buyJewelCard(toBuy))
    #
    # # #-----------------------------------------------------------------------------------------------------------------
    # # At this point, we have zero token in our inventory.
    # # Though we have one SAPPHIRE jewel card (w/ 1 gem)
    #
    # # card to purchase (not enough tokens but enough gold) ✅
    # toBuy = JewelCard(None, 0, 3, 2, [PLAY_AGAIN, CHOOSE_GEMSTONE], requirements={     #Required gemstones/jewels to buy this instance of JewelCard
    #     PEARL           :   1,  # PEARL,
    #     BLUE_SAPPHIRE   :   2,  # SAPPHIRE,
    #     DIAMOND         :   1,  # DIAMOND,
    #     EMERALD         :   0,  # EMERALD,
    #     RUBY            :   0,  # RUBY,
    #     OBSIDIAN        :   0   # OBSIDIAN
    # })
    # inv.addToken(GOLD, 3)
    #
    # print()
    # print("Card to purchase with just enough jewels (no token though):")
    # print(toBuy)
    # print('The following is "inv.buyJewelCard(toBuy)": ')
    # print(inv.buyJewelCard(toBuy))

    # #-----------------------------------------------------------------------------------------------------------------
    # # checking Inventory.nbCrowns() ✅
    # #-----------------------------------------------------------------------------------------------------------------
    # print()
    # print("Inventory.nbCrowns() testing:\nAdding a few cards;")
    # inv.addJewelCard(JewelCard(tokenType = BLUE_SAPPHIRE, nbJewel= 1, nbCrowns=0,nbPrestige=0,abilities=["PlayAgain", "ChooseGemstone"]))
    # inv.addJewelCard(JewelCard(tokenType = BLUE_SAPPHIRE, nbJewel= 1, nbCrowns=2,nbPrestige=0,abilities=[]))
    # inv.addJewelCard(JewelCard(tokenType = BLUE_SAPPHIRE, nbJewel= 1, nbCrowns=1,nbPrestige=0,abilities=[]))
    # print(f"inv.nbCrowns() is equal to: {inv.nbCrowns()} (<-- should be 3)")


    # #-----------------------------------------------------------------------------------------------------------------
    # # checking updated SDGameHandler.addToInventory() ✅
    # #-----------------------------------------------------------------------------------------------------------------
    # # addToInventory(self,  player: int,
    # #                       itemType: int,
    # #                       item: JewelCard | RoyalCard | int)
    # #               -> None:
    # print()
    # print("GAME INVENTORIES")
    # print(game.inventories[0])
    # print(game.inventories[1])
    # print("ADDING STUFF (player 1)")
    # JCardToAdd = JewelCard(None,0,3,3,[],{BLUE_SAPPHIRE: 1},None)
    # RCardToAdd = RoyalCard(3,[], None)
    # game.addToInventory(1,TOKEN,[BLUE_SAPPHIRE,4])
    # game.addToInventory(1,JEWEL_CARD,JCardToAdd)
    # game.addToInventory(1,ROYAL_CARD,RCardToAdd)
    # game.addToInventory(1,BOOKED_CARD,JCardToAdd)
    # game.addToInventory(1,PRIVILEGE,2)
    # print("GAME INVENTORIES")
    # print(game.inventories[0])
    # print(game.inventories[1])
    # print()
    # print("ADDING TOO MUCH STUFF (player 1 still)")
    # game.addToInventory(1, TOKEN, [BLUE_SAPPHIRE, 1])   #should be alright since we consumed 1 sap. to buy the JCard
    # game.addToInventory(1, TOKEN, [BLUE_SAPPHIRE,1])    #should result in an error (too many sapphire tokens)
    # game.addToInventory(1, ROYAL_CARD, RCardToAdd)      #error also here (not enough crowns)
    # game.addToInventory(1, BOOKED_CARD, JCardToAdd)
    # game.addToInventory(1, BOOKED_CARD, JCardToAdd)
    # game.addToInventory(1, BOOKED_CARD, JCardToAdd)     #error (too many booked cards)
    # game.addToInventory(1, PRIVILEGE, 2)                #error (too many privileges)
    # # game.addToInventory(3, PRIVILEGE, 2)                #error, not a player (works ✅)
    # game.addToInventory(1, 5, JCardToAdd)   #error, not an itemType

    # #-----------------------------------------------------------------------------------------------------------------
    # # checking pyramid & data import SDGameHandler.getDecks(), shuffleDecks() & loadPyramid() ✅
    # #-----------------------------------------------------------------------------------------------------------------
    # print()
    # print(f"Game Handler Decks      : {game.decks}")
    # print(f"Game Handler Pyramid    : {game.pyramid}")
    # print(f"Game Handler Royal Cards: {game.royalCards}")
    # print()
    # print("Loading decks")
    # game.loadDecks()
    # print("Shuffling decks")
    # game.shuffleDecks()
    # print("Loading pyramid")
    # game.loadPyramid()
    # print()
    # print(f"Game Handler Decks:")
    # for x in game.decks:
    #     print(f"[length: {len(x)}]{x}")
    # print()
    # print(f"Game Handler Pyramid:")
    # for x in game.pyramid[0]:
    #     print(f"LEVEL 1: {x}")
    # for x in game.pyramid[1]:
    #     print(f"LEVEL 2: {x}")
    # for x in game.pyramid[2]:
    #     print(f"LEVEL 3: {x}")
    # print()
    # print(f"Game Handler Royal Cards:")
    # for x in game.royalCards:
    #     print(f"{x}")
    # print()


    # #-----------------------------------------------------------------------------------------------------------------
    # # checking SDGameHandler.tokenCapture(coords[], player) ✅
    # #-----------------------------------------------------------------------------------------------------------------
    #
    # # Distribution of tokens on the board.
    # game.redistribute()
    # for i in range(5):
    #     print(game.board[i])
    # # Checking whether there's something left in the bank (shouldn't be the case).
    # print(game.bank())
    #
    # # Checking inventory & method (Vertical [DOWN] + 3 gemstones) ✅
    # # WORKS WITH SEED 2
    # print(game.inventories[0])
    # game.tokenCapture([[1,1],[2,1],[3,1]], 1)
    # print(game.inventories[0])
    #
    # # Checking method (Diagonal [DOWN LEFT] + 2 pearls) ✅
    # game.tokenCapture([[0, 1], [1, 2],[2, 3]], 1)
    #
    # # Checking method (Horizontal [LEFT]) ✅
    # game.tokenCapture([ [4, 1],[4, 2], [4, 3]], 1)
    #
    # # Checking method (Vertical (UP), 2 TOKENS) ✅
    # game.tokenCapture([ [2, 4],[1, 4], [-1,-1]], 1)
    #
    # # Checking method (Wrong order -> error) ✅
    # game.tokenCapture([[0,3], [0,2], [0,4] ], 1)
    #
    # # Checking method (Gold token -> error) ✅
    # game.tokenCapture([[0,4], [-1,-1], [-1,-1] ], 1)
    #
    # # Checking method (Another wrong order -> error) ✅
    # game.tokenCapture([[0,0],[-1,-1],[1,0]], 1)
    # game.tokenCapture([[0,0],[2,2],[1,1]],1)
    # # Checking method (Trying to take None -> error) ✅ (UNEXPECTED: Takes the first token anyway!
    #                                                     # UPDATE   : Doesn't matter, we'll end the game after this error)
    # game.tokenCapture([[0,0], [0,1], [0,2]],1)
    #
    # # Checking method (wrong format -> error) ✅
    # game.tokenCapture([[0,0,0], [0], [-1,-1]], 1)
    #
    # # Checking method (wrong format -> error) ✅
    # game.tokenCapture([[0,0], [0], [-1,-1]], 1)
    #
    # # Checking method (wrong coordinates -> error) ✅
    # game.tokenCapture([[0,11], [0,12], [-1,-1]], 1)
    #
    # # Checking method (not aligned -> error) ✅
    # game.tokenCapture([[3,2],[3,3],[4,4]],1)
    #
    # # Checking method (shouldn't use [-1,-1] -> error) ✅
    # game.tokenCapture([[-1,-1],[-1,-1],[-1,-1]], 1)     # ✅
    # game.tokenCapture([[-1,-1], [-2,-2]], 1)            # ✅
    #
    # # Checking method (only one coordinate given) ✅
    # game.tokenCapture([[4,4]],1)
    #
    # # Checking method (strs/chars instead of ints) ✅
    # game.tokenCapture([['a','b']],1)
    #
    #
    # for i in range(5):
    #     print(game.board[i])

    # #-----------------------------------------------------------------------------------------------------------------
    # # Display of cards. Will be useful to elaborate print method ✅
    # #-----------------------------------------------------------------------------------------------------------------
    #
    # # Cards w/ emojis.
    # # Reminder of the only card w/ 2 abilities:
    # # "level3": [
    # #     {
    # #         "tokenType": null,
    # #         "nbJewel": 1,
    # #         "nbPrestige": 3,
    # #         "nbCrowns": 0,
    # #         "abilities": ["ChooseGemstone", "PlayAgain"],
    # #         "requirements": [0, 0, 0, 0, 8, 0],
    # #         "_comment": "req=[PEARL,SAPPHIRE,DIAMOND,EMERALD,RUBY,OBSIDIAN]"
    # #     }
    # # ]
    #
    #
    # # print("┌───────────┐")
    # # print("│✨3 👑0 🃏1│")
    # # print("│           │")
    # # print("│        ❗ │")
    # # print("│       💎🔄│")
    # # print("│🔴8        │")
    # # print("└───────────┘")
    #
    # #two abilities
    # test1 = JewelCard(None,1,3,0,[CHOOSE_GEMSTONE,PLAY_AGAIN],{RUBY: 8},None)
    #
    # #no ability (actually it's a blank card)
    # test2 = JewelCard(None,0,0,0,[],{},None)
    #
    # #one ability
    # test3 = JewelCard(None,1,3,2,["ChooseGemstone"],{RUBY: 8,PEARL:1},None)
    #
    # #another one
    # test4 = JewelCard(BLUE_SAPPHIRE,1,3,2,["ChooseGemstone","GetAPrivilegeScroll"],{RUBY: 8,PEARL:1},None)
    #
    # strsAbilities = []
    #
    # test = test3 #proxy just to change the number instead of changing it everywhere
    # print(test.abilities)
    #
    #
    # # Ability display
    # match test.abilities[0]:
    #     case 0:
    #         #nothing
    #         strsAbilities += ["  ","  "]
    #     case 1:
    #         #play again
    #         strsAbilities += ["❗","🔄"]
    #     case 2:
    #         #choose gemstone
    #         strsAbilities += ["❗", "💎"]
    #     case 3:
    #         #take token
    #         strsAbilities += ["❗", "🪙"]
    #     case 4:
    #         #privilege
    #         strsAbilities += ["❗", "🗞️"]
    #     case 5:
    #         #steal gemstone
    #         strsAbilities += ["❗", "🫳"]
    #
    # print(strsAbilities)
    # match test.abilities[1]:
    #     case 0:
    #         strsAbilities[1] = f" {strsAbilities[1]} "
    #     case 1:
    #         strsAbilities[1] = f"{strsAbilities[1]}🔄"
    #     case 2:
    #         strsAbilities[1] = f"{strsAbilities[1]}💎"
    #     case 3:
    #         strsAbilities[1] = f"{strsAbilities[1]}🪙"
    #     case 4:
    #         strsAbilities[1] = f"{strsAbilities[1]}🗞️"
    #     case 5:
    #         strsAbilities[1] = f"{strsAbilities[1]}🫳"
    #
    #
    # #top of the card
    # strsTop = []
    # if test.nbPrestige:
    #     strsTop.append(f"✨{test.nbPrestige}")
    # else:
    #     strsTop.append("   ")
    #
    # if test.nbCrowns:
    #     strsTop.append(f"👑{test.nbCrowns}")
    # else:
    #     strsTop.append("   ")
    #
    # if test.nbJewel:
    #     strsTop.append(f"{tokenEmojis[0][test.tokenType]}{test.nbJewel}")
    # else:
    #     strsTop.append("   ")
    #
    #
    # # Required tokens display
    # strsTokens = ["   ","   ","   ","   "]
    # i=0
    # for key in test.requirements:
    #     if test.requirements[key]:
    #         strsTokens[i] = f"{tokenEmojis[0][key]}{test.requirements[key]}"
    #         i += 1
    #
    # cardStrList = [
    #             f"┌───────────┐",
    #             f"│{strsTop[0]} {strsTop[1]} {strsTop[2]}│",
    #             f"│{strsTokens[3]}        │",
    #             f"│{strsTokens[2]}     {strsAbilities[0]} │",
    #             f"│{strsTokens[1]}    {strsAbilities[1]}│",
    #             f"│{strsTokens[0]}        │",
    #             f"└───────────┘"
    # ]
    #
    # print("WillItCrash.py")
    # for x in cardStrList:
    #     print(x)
    #
    # print("JewelCard.cardDraw()")
    # for x in test.cardDraw(False):
    #     print(x)
    # # check if nbJewel >= 10 (takes more space!)
    # # nvm no card does have a nbJewel >= 10
    # #-----------------------
    # # COLOR CONSTANTS TO ADD
    # # (ROUND=0, SQUARE=1)
    # # colorToken[SHAPE][key]
    # #-----------------------
    # # tokenTypesDict = {
    # # "None"          :    None,
    # # "Pearl"         :    PEARL,         🟣🟪
    # # "Gold"          :    GOLD,          🟡🟨
    # # "Blue Sapphire" :    BLUE_SAPPHIRE, 🔵🟦
    # # "Diamond"       :    DIAMOND,       ⚪⬜
    # # "Emerald"       :    EMERALD,       🟢🟩
    # # "Ruby"          :    RUBY,          🔴🟥
    # # "Obsidian"      :    OBSIDIAN,      ⚫⬛

    # #-----------------------------------------------------------------------------------------------------------------
    # # checking SDGameHandler.printPyramid()   ✅
    # # checking SDGameHandler.printInventory() ✅
    # #-----------------------------------------------------------------------------------------------------------------

    # print()
    # print(f"Game Handler Decks      : {game.decks}")
    # print(f"Game Handler Pyramid    : {game.pyramid}")
    # print(f"Game Handler Royal Cards: {game.royalCards}")
    # print()
    # print("Loading decks")
    # game.loadDecks()
    # print("Shuffling decks")
    # game.shuffleDecks()
    # print("Loading pyramid")
    # game.loadPyramid()
    # print()
    # print(f"Game Handler Decks:")
    # for x in game.decks:
    #     print(f"[length: {len(x)}]{x}")
    # print()
    # print(f"Game Handler Pyramid:")
    # for x in game.pyramid[0]:
    #     print(f"LEVEL 1: {x}")
    # for x in game.pyramid[1]:
    #     print(f"LEVEL 2: {x}")
    # for x in game.pyramid[2]:
    #     print(f"LEVEL 3: {x}")
    # print()
    # print(f"Game Handler Royal Cards:")
    # for x in game.royalCards:
    #     print(f"{x}")
    # print()
    # print("Testing SDGameHandler.printPyramid()")
    # print(game.strPyramid(False))
    # print(game.strPyramid(True))
    #
    # game.redistribute()
    # #for i in range(5):
    # #    print(game.board[i])
    # #print(game.bank())
    #
    # print("Testing SDGameHandler.printInventory()")
    # game.tokenCapture([ [4, 1],[4, 2], [4, 3]], 1)
    # game.tokenCapture([ [2, 4],[1, 4], [-1,-1]], 1)
    #
    # JCardToAdd = JewelCard(BLUE_SAPPHIRE,1,3,3,[],{BLUE_SAPPHIRE: 1},None)
    # # RCardToAdd = RoyalCard(3,["ChooseGemstone"], None)
    # RCardToAdd = game.royalCards[1]
    # game.addToInventory(1,TOKEN,[BLUE_SAPPHIRE,4])
    # print("not yet in inventory:")
    # print(game.strRoyalCards(False))
    # game.addToInventory(1,ROYAL_CARD,RCardToAdd)
    # print("one in inventory:")
    # print(game.strRoyalCards(False))
    # game.addToInventory(1,ROYAL_CARD,RCardToAdd)
    # print("two in inventory:")
    # print(game.strRoyalCards(False))
    # JCardToAdd1 = JewelCard(BLUE_SAPPHIRE,3,3,3,["ChooseGemstone","PlayAgain"],{BLUE_SAPPHIRE: 1},None)
    # game.addToInventory(1,JEWEL_CARD,JCardToAdd1)
    # game.addToInventory(1,ROYAL_CARD,RCardToAdd)
    # game.addToInventory(1,BOOKED_CARD,JCardToAdd1)
    # game.addToInventory(1,BOOKED_CARD,JCardToAdd1)
    # game.addToInventory(1,BOOKED_CARD,JCardToAdd)
    # game.addToInventory(1,PRIVILEGE,2)
    # game.addToInventory(1, TOKEN, [BLUE_SAPPHIRE, 1])   #should be alright since we consumed 1 sap. to buy the JCard
    #
    # #for x in RCardToAdd.cardDraw(False):
    # #    print(x) ```
    #
    # print(game.strInventory(1,True,False))
    # print(game.strInventory(1,True,True))
    # print(game.strInventory(2,False,False))
    # print(game.strInventory(2,False,True))
    # print(game.strRoyalCards(False))
    # #for x in game.alignStrCards([JCardToAdd,JCardToAdd1], True):
    # #    print(x)
    #
    # # game.royalCards.pop(1)
    #
    # #There may or may not be a mismatch between prestige points displayed & the total. Total also accounts for royal cards, which is the case here!
    # print()
    # print("Testing SDGameHandler.strPlayerDisplay()")
    # # print(game.strPlayerDisplay(1,True))
    # print(game.strPlayerDisplay(1,False))
    #
    # # print("Testing SDGameHandler.strBoard()")
    # # print(game.strBoard(False))


    # -----------------------------------------------------------------------------------------------------------------
    # Checking SDGameHandler.buyBookedCard() ✅
    # -----------------------------------------------------------------------------------------------------------------
    emoji = False
    print()
    print(f"Game Handler Decks      : {game.decks}")
    print(f"Game Handler Pyramid    : {game.pyramid}")
    print(f"Game Handler Royal Cards: {game.royalCards}")
    print()
    print("Loading decks")
    game.loadDecks()
    print("Shuffling decks")
    game.shuffleDecks()
    print("Loading pyramid")
    game.loadPyramid()
    print()


    print("Adding stuff in player1's inventory")
    RCardToAdd = game.royalCards[1]
    JCardToBook = JewelCard(BLUE_SAPPHIRE,3,10,3,["ChooseGemstone","PlayAgain"],{BLUE_SAPPHIRE: 1},None)
    game.addToInventory(1,BOOKED_CARD,JCardToBook)

    print("Dispatching tokens on the board")
    game.distribute()
    print(game.strBoard(emoji))
    print("Capturing a blue token on the board (player 1)")
    game.tokenCapture([ [0, 1],[-1, -1], [-1, -1]], 1)
    # If random changes, use next line:
    # game.addToInventory(1,TOKEN,[BLUE_SAPPHIRE,1])
    print(game.strBoard(emoji))
    print("Display (player1's POV):")
    print(game.strPlayerDisplay(1,emoji))

    print("Testing SDGameHandler.buyBookedCard()\nBefore purchase:")
    print(game.strPlayerDisplay(1,emoji))
    print()
    game.buyBookedCard(1,0)
    print()
    print("After buying booked card:")
    print(game.strPlayerDisplay(1,emoji))
    print(game.inventories[0].bookedCards)

    print(game.strInventory(2,1,True))