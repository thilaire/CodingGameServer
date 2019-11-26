//
// Created by Thib on 30/10/2019.
//

// Correspond à la question 1 (jouer à la main contre le serveur)



#include <stdio.h>
#include <stdlib.h>
#include "snakeAPI.h"



extern int debug;	/* hack to enable debug messages */


int main()
{
//	char* arena;            /* arena */
	char gameName[50];
	int* walls;            /* array of walls */
	t_return_code ret = NORMAL_MOVE;		/* indicates the status of the previous move */
	t_move move;						    /* a move */
	int player;
	int sizeX,sizeY, nbWalls;
	int X,Y,oX,oY;

	debug=1;	/* enable debug */

	/* connection to the server */
	connectToServer( "localhost", 1235, "TH_test");
	printf("Youhou, connecté au serveur !\n");


	/* wait for a game, and retrieve informations about it */
	//waitForLabyrinth( "PLAY_RANDOM timeout=100 rotate=False tot=25", labName, &sizeX, &sizeY);
	waitForSnakeGame( "RANDOM_PLAYER difficulty=2 timeout=100 seed=42 start=0", gameName, &sizeX, &sizeY, &nbWalls);
//	arena = (char*) calloc( sizeX * sizeY );
	walls = (int*) malloc( nbWalls * 4 * sizeof(int));
	player = getSnakeArena( walls);

	do {

		/* display the game */
		printArena();

		if (player==1)	/* The opponent plays */
		{
			ret = getMove( &move);
			//playMove( arena, move);
		}
		else
		{
			//.... choose what to play
			printf("\nIt's your turn to play (0:NORTH, 1:EAST, 2:SOUTH, 3:WEST):");
			scanf("%d", &move);
			ret = sendMove(move);
			//playMove( arena, move);
		}

		/* change player */
		player = ! player;

	} while (ret==NORMAL_MOVE);

	if ( (player==0 && ret==WINNING_MOVE) || (player==1 && ret==LOOSING_MOVE) )
		printf("\n Unfortunately, the opponent wins\n");
	else
		printf("\n Héhé, I win!!\n");

	/* we do not forget to free the allocated array */
	free(walls);


	/* end the connection, because we are polite */
	closeConnection();

	return EXIT_SUCCESS;
}

