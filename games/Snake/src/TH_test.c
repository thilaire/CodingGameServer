//
// Created by Thib on 05/12/2019.
//

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
	srand(time(NULL));

	/* connection to the server */
	connectToServer( "localhost", 1234, "TH_test");

	/* play forever */
	//while(1){

		/* new game */
		game = (t_game*) malloc(sizeof(t_game));
		/* wait for a game, and retrieve informations about it */
		waitForSnakeGame( "RANDOM_PLAYER difficulty=3 timeout=100  start=0", gameName, &sizeX, &sizeY, &nbWalls);
		/* get the walls and build the game */
		walls = (int*) malloc( nbWalls * 4 * sizeof(int));
		game->player = getSnakeArena( walls);
		buildGame(game, walls, nbWalls, sizeX, sizeY);
		free(walls);

		/* let's play !! */
		do {

			/* display the game */
			printArena();
			//displayArena(game);

			if (game->player) {/* The opponent plays */
				ret = getMove( &move);
			}
			else {
				move = getRandomMove(game);
				//move = bestMove(game);
				//printf("\nIt's your turn to play (0:NORTH, 1:EAST, 2:SOUTH, 3:WEST):");
				//scanf("%d", &move);
				ret = sendMove(move);
			}
			if (ret==NORMAL_MOVE)
				playMove(game, move);

		} while (ret==NORMAL_MOVE);

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

