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
 * - labyrinthName: char* to get the game Name (should be allocated, max 50 characters),
 *
 * - nbCities: to get the number of cities
 * - nbTracks: to get the number of tracks between the cities
 */
void waitForT2RGame( char* gameType, char* labyrinthName, int* nbCities, int* nbTracks)
{
	char data[10];
	/* wait for a game */
	waitForGame( __FUNCTION__, gameType, labyrinthName, data);

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
 * - tracks: array of t_tracks
 *   (the pointers data MUST HAVE allocated with the right size !!)
 *
 * Returns 0 if you begin, or 1 if the opponent begins
 */
int getMap(t_track* tracks)
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
		strcpy(*name, city);
		name++;
	}

	/* copy the data in the tracks array */
	for(int i=0; i < nbTr; i++){
		sscanf(p, "%d %d %d %d %d %n", tracks->cities, tracks->cities+1, &tracks->length, tracks->colors, tracks->colors+1, &nbchar);
		tracks++;
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