/*

Here is the API you gave to the players

With that API, they can connect to the server, play move, display the game, send comments, etc.

*/

#include "clientAPI.h"
#include <stdio.h>
#include "caVaPlanterAPI.h"



/* -------------------------------------
 * Initialize connection with the server
 * Quit the program if the connection to the server cannot be established
 *
 * Parameters:
 * - serverName: (string) address of the server (it could be "localhost" if the server is run in local, or "pc4521.polytech.upmc.fr" if the server runs there)
 * - port: (int) port number used for the connection
 * - name: (string) name of the player : max 20 characters (checked by the server)
 */
void connectToServer( char* serverName, int port, char* name)
{
	connectToCGS( __FUNCTION__, serverName, port, name);
}


/* ----------------------------------
 * Close the connection to the server
 * to do, because we are polite
 *
 * Parameters:
 * None
*/
void closeConnection()
{
	closeCGSConnection( __FUNCTION__ );
}


/* ----------------------------------------------------------------
 * Wait for a Game, and retrieve its name and first data
 * (typically, array sizes)
 *
 * Parameters:
 * - gameType: string (max 50 characters)
 * - labyrinthName: string (max 50 characters),
 *                  corresponds to the game name
 * - insert your size data here...
 *
 * gameType is a string like "NAME key1=value1 key2=value1 ..."
 * - NAME can be empty. It gives the type of the training player
 * - key=value pairs are used for options
 *   (each training player has its own options)
 *   invalid keys are ignored, invalid values leads to error
 *   the following options are common to every training player
 *   (when NAME is not empty or not TOURNAMENT):
 *        - 'timeout': allows an define the timeout
 *                   when training (in seconds)
 *        - 'seed': allows to set the seed of the random generator
 *        - 'start': allows to set who starts ('0' or '1')
 * gameType could also be : "TOURNAMENT name" where name is the name of the tournament
  */
void waitForSplendorGame( char* gameType, char* labyrinthName, ...)
{
	char data[...];
	/* wait for a game */
	waitForGame( __FUNCTION__, gameType, labyrinthName, data);

}


/* -------------------------------------
 * Get the data and tell who starts
 *
 * Parameters:
 * - data: pointer to data to fill
 *   (the pointer data MUST HAVE allocated with the right size !!)
 *
 * Returns 0 if you begin, or 1 if the opponent begins
 */
int getSplendorGameData( ...) //tableau de 150 char
{
	char data[N];   /* size to define */
	/* wait for a game */
	int ret = getGameData( __FUNCTION__, data, N);

	/*
	 * insert your code to copy the data in the player data
	 25 ints then 5*12 ints (5 level-1 Jewel Cards), 4*12 ints (4 level-2 JCards), 3*12 (3 level-3 JCards), 4*2 ints (4 royal cards)
	 */
	//mettre dans le tableau à retourner grâce aux valeurs qui sont dans data. 
	//À mettre dedans avec sscanf()
	//bheck snakepapi.c

	//datra : chaine de char que je vais lire avec sscanf

	//faiore la meme chose pour getmove()
	//quasi la même pour sendmove, sauf qy'on la construit. On l'envoie avec SendCGSMove()

    return ret;
}



/* ----------------------
 * Get the opponent move
 *
 * Parameters:
 * - move: a move
 *
 * Returns a return_code
 * NORMAL_MOVE for normal move,
 * WINNING_MOVE for a winning move, -1
 * LOOSING_MOVE for a losing (or illegal) move
 * this code is relative to the opponent (WINNING_MOVE if HE wins, ...)
 */
t_return_code getMove( t_move* move )
{

    char data[N];   /* to define */

    /* get the move */
    int ret = getCGSMove( __FUNCTION__, data, N);

	/*
	 * insert your code to extract move from the data
	 */

	return ret;
}



/* -----------
 * Send a move
 *
 * Parameters:
 * - move: a move
 *
 * Returns a return_code
 * NORMAL_MOVE for normal move,
 * WINNING_MOVE for a winning move, -1
 * LOOSING_MOVE for a losing (or illegal) move
 * this code is relative to your programm (WINNING_MOVE if YOU win, ...)
 */
t_return_code sendMove( t_move move )
{
    char data[...];

    /*
     * insert your code to build the string data from the move
     */

	/*
	Optional moves (choose between 0 to 2 move(s)):
		- Take a Token: "1to x y"
		If there's nothing to catch, enter (-1,-1).
		It'll consume one privilege scroll.
		- Redistribute: "rd"
		- None        : (don't send anything then)

	Mendatory moves
		- Take Tokens: "to x1 y1 x2 y2 x3 y3"
		- Book a card: "book [level] [index of the card]"
			If you want to take from the decks, choose only the level of the card
		- Buy a JCard: "buy [level] [index]"
		- Royal Card : "royal [index]"
			To use only after reaching 3 or 6 crowns			
	*/

    /* send the move */
	return sendCGSMove( __FUNCTION__, data);
}




/* ----------------------
 * Display the Game
 * in a pretty way (ask the server what to print)
 */
void printSplendorGame()
{
    printGame( __FUNCTION__ );
}



/* ----------------------------
 * Send a comment to the server
 *
 * Parameters:
 * - comment: (string) comment to send to the server (max 100 char.)
 */
void sendComment(char* comment)
{
    sendCGSComment( __FUNCTION__, comment);
}
