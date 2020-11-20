/*
+----------------------------------------------------+
|                                                    |
|        #######                                     |
|           #    #  ####  #    # ###### #####        |
|           #    # #    # #   #  #        #          |
|           #    # #      ####   #####    #          |
|           #    # #      #  #   #        #          |
|           #    # #    # #   #  #        #          |
|           #    #  ####  #    # ######   #          |
|                                                    |
|                      ######                        |
|      #####  ####     #     # # #####  ######       |
|        #   #    #    #     # # #    # #            |
|        #   #    #    ######  # #    # #####        |
|        #   #    #    #   #   # #    # #            |
|        #   #    #    #    #  # #    # #            |
|        #    ####     #     # # #####  ######       |
|                                                    |
|                                                    |
+----------------------------------------------------+

Authors: T. Hilaire
Licence: GPL

File: TicketToRide.h
	Client API for the TicketToRide game with CGS

Copyright 2020 T. Hilaire
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "clientAPI.h"
#include "TicketToRideAPI.h"


/* global variables used in intern, so the user do not have to pass them once again) */
int nbTr;        /* number of tracks */
int nbC;		/* number of cities */
char** cityNames;	/* array of city names */


/* -----------------------
 * Dummy function that does
 * a string copy (exactly as strcpy)
 * but replace the '_' by ' ' in the same time
 * it does the copy
 */
void strCpyReplace(char* dest, const char* src)
{
	while(*src) {
		if (*src != '_')
			*dest++ = *src;
		else
			*dest++ = ' ';
		src++;
	}
}



/* -------------------------------------
 * Initialize connection with the server
 * Quit the program if the connection to the server
 * cannot be established
 *
 * Parameters:
 * - serverName: (string) address of the server
 * - port: (int) port number used for the connection
 * - name: (string) name of the bot : max 20 characters
 */
void connectToServer(char* serverName, int port, char* name)
{
	connectToCGS(__FUNCTION__, serverName, port, name);
}


/* ----------------------------------
 * Close the connection to the server
 * because we are polite
 *
 */
void closeConnection()
{
	/* free the data */
	char** p = cityNames;
	for(int i=0; i<nbC; i++)
		free(*p++);
	free(cityNames);
	/* close the connection */
	closeCGSConnection(__FUNCTION__);
}


/* ----------------------------------------------------------------
 * Wait for a T2R Game, and retrieve its name and first data
 * (the number of cities and the number of connections)
 *
 * Parameters:
 * - gameType: string (max 200 characters) type of the game we want to play
 *             (empty string for regular game)
 *             "TRAINING xxxx" to play with the bot xxxx
 *             "TOURNAMENT xxxx" to join the tournament xxxx
 *     gameType can also contains extra data in form "key1=value1 key2=value1 ..."
 *     to provide options (to bots)
 *     invalid keys are ignored, invalid values leads to error
 *     the following options are common to every training player
 *        - 'timeout': allows an define the timeout when training (in seconds)
 *        - 'seed': allows to set the seed of the random generator
 *        - 'start': allows to set who starts ('0' or '1')
 *     the following bots are available:
 *        - DO_NOTHING (stupid player what withdraw cards)
 *
 * - gameName: char* to get the game Name (should be allocated, max 50 characters),
 *
 * - nbCities: to get the number of cities
 * - nbTracks: to get the number of tracks between the cities
 */
void waitForT2RGame(char* gameType, char* gameName, int* nbCities, int* nbTracks)
{
	char data[10];
	/* wait for a game */
	waitForGame(__FUNCTION__, gameType, gameName, data);

	/* parse the data */
	sscanf(data, "%d %d", nbCities, nbTracks);
	nbTr = *nbTracks;
	nbC = *nbCities;
	cityNames = (char**) malloc(nbC*sizeof(char*));
}


/* -------------------------------------
 * Get the map and tell who starts
 *
 * Parameters:
 * - tracks: array of (5 x number of tracks) integers
 * 		Five integers are used to define a track:
 * 		- (1) id of the 1st city
 * 		- (2) id of the 2nd city
 * 		- (3) length of the track (between 1 and 6)
 * 		- (4) color of the track (MULTICOLOR if any color can be used)
 * 		- (5) color of the 2nd track if the track is double (NONE if the track is not a double track)
 *
 *   (the pointers data MUST HAVE allocated with the right size !!)
 *
 * Returns 0 if you begin, or 1 if the opponent begins
 */
int getMap(int* tracks)
{
	char data[4096];   /* 16 char per track, 256 tracks max */
	int nbchar;
	char *p, **name;
	char city[20];

	/* wait for a game */
	int ret = getGameData( __FUNCTION__, data, 4096);

	/* copy the city's names */
	p = data;
	name = cityNames;
	for(int i=0; i < nbC; i++){
		sscanf(p, "%s%n", city, &nbchar);
		p += nbchar;
		*name = (char*) malloc(strlen(city)+1);
		strCpyReplace(*name++, city);
	}

	/* copy the data in the tracks array */
	for(int i=0; i < nbTr; i++){
		sscanf(p, "%d %d %d %d %d %n", tracks, tracks+1, tracks+2, tracks+3, tracks+4, &nbchar);
		tracks += 5;
		p += nbchar;
	}

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

    char data[256];   /* to define */

    /* get the move */
    int ret = getCGSMove( __FUNCTION__, data, 256);

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
    char data[256];

    /*
     * insert your code to build the string data from the move
     */

    /* send the move */
	return sendCGSMove( __FUNCTION__, data);
}




/* ----------------------
 * Display the Game
 * in a pretty way (ask the server what to print)
 */
void printMap()
{
	printCGSGame(__FUNCTION__);
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

/* --------------------
 * Display a city's name
 * Parameters:
 * - city: (int) id of the city
 */
void printCity(int city){
	printf("%s", cityNames[city]);
}

