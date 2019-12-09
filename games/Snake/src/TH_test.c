//
// Created by Thib on 05/12/2019.
//
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "snakeAPI.h"
#include "arena.h"

extern int debug;

int main()
{
	t_game* game;            /* arena */
	char gameName[50];
	int* walls;            /* array of walls */
	t_return_code ret = NORMAL_MOVE;		/* indicates the status of the previous move */
	t_move move;						    /* a move */
	int sizeX,sizeY, nbWalls;
debug=0;

	srand(time(NULL));	/* random initialized from time */

	/* connection to the server */
	connectToServer( "localhost", 1234, "TH_test");

	/* play forever */
	//while(1){

		/* new game */
		game = (t_game*) malloc(sizeof(t_game));
		/* wait for a game, and retrieve informations about it */
		waitForSnakeGame( "SUPER_PLAYER difficulty=5 timeout=100 seed=0 start=0", gameName, &sizeX, &sizeY, &nbWalls);
		/* get the walls and build the game */
		walls = (int*) malloc( nbWalls * 4 * sizeof(int));
		game->player = (uint8_t) getSnakeArena( walls);
		initGame(game, walls, nbWalls, (uint8_t)sizeX, (uint8_t)sizeY);
		free(walls);

		/* let's play !! */
		do {

			/* display the game */
			printArena();
			//displayArena(game);

			/* The opponent plays */
			if (game->player)
				ret = getMove( &move);
			else {
				/* or we play */
				//move = getRandomMove(game);
				move = getOneRoundBestMove(game);
				ret = sendMove(move);
			}
			/* update the game */
			if (ret==NORMAL_MOVE)
				playMove(game, move);

		} while (ret==NORMAL_MOVE);

		/* show who wins */
		if ( (game->player==0 && ret==WINNING_MOVE) || (game->player==1 && ret==LOOSING_MOVE) )
			printf("\n Héhé, I win!!\n");
		else
			printf("\n Unfortunately, the opponent wins\n");

		/* we do not forget to free the allocated array */
		freeGame(game);

		//}

	/* end the connection, because we are polite */
	closeConnection();

	return EXIT_SUCCESS;
}

