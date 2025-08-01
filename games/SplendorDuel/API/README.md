 # Splendor Duel

## This game is an adaptation of [Splendor Duel](https://www.spacecowboys.fr/splendor-duel-en) for Coding Game Server.

### Cards

First, it is useful to note that when printing the display (using `printSplendorGame()`),
```
      ┌───────────┐          ┌───────────┐
      │PP3 CR3 GM3│          │✨3 👑3 🟦3│
      │           │          │           │
 this │        !! │ and this │        ❗ │
      │       CGPA│          │       💎🔄│
      │B1         │          │🔵1        │
      └───────────┘          └───────────┘
```
are the two depictions of the same Jewel Card. The depiction changes depending on the `emoji` parameter when calling the function and you should see different colours in the terminal in the first depiction.

The second depiction is working fine on Kubuntu (Ubuntu with the KDE Plasma desktop environment). It'll most likely work fine with a vanilla Ubuntu.

However, if you want reliability in the depiction (i.e. not having to deal with misaligned texts & tables), I recommend not using emojis, as they don't always show properly (e.g. on Mac, the display is unusable). Try this yourself, it is a simple print statement so if it doesn't work, you can always switch back.

All of these represent (left to right, top to bottom):

- PPx or ✨x : number of Prestige Points of the card.

- CRx or 👑x : number of Crowns of the card.

- GMx or 🟦x: Gems of the card (colors of GM & emoji may vary, see first table below)

- !! or❗: alerts that there is at least one special ability, listed just below the exclamation mark.
 
- CGPA or 💎🔄: two special abilities. All the abilities are listed below in the second table.

- Bx or 🔵x: number of tokens (Blue Sapphire tokens here) and/or permanent gem bonuses required in order to purchase the card. All the gem colors are listed below.

#### Table 1: Jewel Card Gem emoji signification
| Emoji = True | Emoji = False | Meaning       |
|--------------|---------------|---------------|
| 🃏           | N             | None          |
| 🟪           | P             | Pearl         |
| 🟦           | B             | Blue Sapphire |
| ⬜           | D             | Diamond       |
| 🟩           | E             | Emerald       |
| 🟥           | R             | Ruby          |
| ⬛           | O             | Obsidian      |
Please note that when not using emojis, letters are written in a color similar to the one in the emoji column (e.g. `P` is written in purple, `O` in black & whatnot)

#### Table 2: Jewel Card Ability list
| Emoji = True | Emoji = False | Meaning                                  |
|--------------|---------------|------------------------------------------|
| ❗           | !!            | Informs about the presence of an ability |
| 🔄           | PA            | Play Again                               |
| 💎           | CG            | Choose Gem (of the card)                 |
| 🪙           | TT            | Take a Token (on the board)              |
| 🗞️           | PS            | get a Privilege Scroll                   |
| 🫳           | ST            | Steal a Token from your opponent         |


#### Table 3: Token emoji signification 
| Emoji = True | Emoji = False | Meaning             |
|--------------|---------------|---------------------|
| 🟣           | P             | Pearl token         |
| 🟡           | G             | Gold token          |
| 🔵           | B             | Blue Sapphire token |
| ⚪           | D             | Diamond token       |
| 🟢           | E             | Emerald token       |
| 🔴           | R             | Ruby token          |
| ⚫           | O             | Obsidian token      |
Please note that when not using emojis, letters are written in a color similar to the one in the emoji column (e.g. `P` is written in purple, `G` in yellow & whatnot)

### Inventory

Same goes for the inventory. This :
```
┌──────────────────────PLAYER x────────────────────────────┐
│ - Tokens        :      P0,  G0,  B0,  D0,  E0,  R0,  O0  │
│ - Cards (jewels):                B0,  D0,  E0,  R0,  O0  │
│ - Prestige      : Total: 0,  N0, B0,  D0,  E0,  R0,  O0  │
│ - Privileges    : 0                                      │
│ - Crowns        : 0                                      │
│ - Booked cards  : 0                                      │
└──────────────────────────────────────────────────────────┘
```

and this :
```
┌──────────────────────PLAYER x────────────────────────────┐
│ - Tokens        :     🟣0, 🟡0, 🔵0, ⚪0, 🟢0, 🔴0, ⚫0  │
│ - Cards (jewels):               🟦0, ⬜0, 🟩0, 🟥0, ⬛0  │
│ - Prestige      : Total: 0,  🃏0,🟦0, ⬜0, 🟩0, 🟥0, ⬛0  │
│ - Privileges    : 🗞️ 0                                   │
│ - Crowns        : 👑 0                                   │
│ - Booked cards  : 0                                      │
└──────────────────────────────────────────────────────────┘
```

are two depictions of the same inventory. 

Let's break it down : 

#### Table 4: Inventory breakdown
| Line           | Meaning                                                                                                                                                                                                                                                          |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tokens         | Number of tokens of a certain type. Whenever you buy a card (and you don't have enough Jewels for the card), they are used. They then go back to the bank, which collects all the tokens to redistribute on the board (which can be done with `redistribute()`.) |
| Cards (jewels) | Number of jewels of a certain type. When purchasing a card, we check how many jewels you own. If you have enough, the card is yours. However, if you do not have enough, we check for tokens (the latter of which will be used after the purchase).              |
| Prestige       | Number of prestige points. You win when reaching 25 prestige points total, 10 in a single jewel colour or 10 crowns. See the rules for a better explanation.                                                                                                     |
| Privileges     | Number of privilege scrolls. Note that you can have 3 maximum. If there's not enough privilege scrolls on the board anymore, it'll be taken from the opponent's inventory.                                                                                       |
| Crowns         | Number of crowns (gained by purchasing jewel cards)                                                                                                                                                                                                              |
| Booked Cards   | Number of cards you have reserved. Note that it isn't mandatory to purchase a card you booked. 3 booked cards maximum per player. Whenever reaching, you should take a gold token on the board.                                                                  |

