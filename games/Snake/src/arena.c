#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "arena.h"
#include "utils.h"


#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))


/* array of shift to apply on indexes xy to get the adjacent xy indexes in a given direction */
int8_t tab_dxy[4] = {0};



/* build the arena from the list of walls given by the server */
void initGame(t_game *game, int *walls, int nbWalls, uint8_t sizeX, uint8_t sizeY){
	int x1, x2, y1, y2;
	/* copy the sizes */
	game->sizeX = sizeX;
	game->sizeY = sizeY;
	/* build tab_dxy */
	tab_dxy[0] = -sizeX;
	tab_dxy[1] = +1;
	tab_dxy[2] = sizeX;
	tab_dxy[3] = -1;
	/* int the arena with walls */
	game->arena = (t_box*) calloc(sizeX*sizeY, sizeof(t_box));
	for(int i=0; i<nbWalls; i++){
		x1 = MIN(walls[i*4],walls[i*4+2]);
		y1 = MIN(walls[i*4+1],walls[i*4+3]);
		x2 = MAX(walls[i*4],walls[i*4+2]);
		y2 = MAX(walls[i*4+1],walls[i*4+3]);
		if (x1==x2){
			game->arena[y1*sizeX+x1].walls |= SOUTH;
			game->arena[y2*sizeX+x2].walls |= NORTH;
		}
		if (y1==y2){
			game->arena[y1*sizeX+x1].walls |= EAST;
			game->arena[y2*sizeX+x2].walls |= WEST;
		}
	}
	/* add the extern walls */
	for(int x=0; x<sizeX; x++){
		game->arena[x].walls |= NORTH;
		game->arena[(sizeY-1)*sizeX+x].walls |= SOUTH;
	}
	for(int xy=0; xy<sizeX*sizeY; xy+=sizeX){
		game->arena[xy].walls |= WEST;
		game->arena[xy+sizeX-1].walls |= EAST;
	}
	/* initial positions of the snakes */
	game->heads[0] = (t_xy) (2 + sizeY/2*sizeX);
	game->heads[1] = (t_xy) (sizeX - 3 + sizeY/2*sizeX);
	game->arena[game->heads[0]].xtra |= 0b011;  /* head of the snake */
	game->arena[game->heads[1]].p = 0;
	game->arena[game->heads[1]].xtra |= 0b011;  /* head of the snake */
	game->arena[game->heads[1]].p = 1;
	/* init the counters */
	game->counters[0] = game->counters[1] = 0;
	/* allocate data for the color and stack arrays */
	allocateUtilsArray(sizeX,sizeY);
}


/* free the allocated memory */
void freeGame(t_game* game){
	free(game->arena);
	free(game);
	freeUtilsArray();
}


/* play a move (update the game)
No need to check if the move is legal or not */
void playMove(t_game* game, t_move move){
	/* new head */
	t_xy xy = game->heads[game->player];
	t_xy oldxy = xy;
	t_xy nh = xy + tab_dxy[move];
	game->heads[game->player] = nh;
	game->arena[nh].p = game->player;
	game->arena[nh].xtra = (uint8_t) 0b100 | ((move+2)&3);
	/* remove the queue (or not) */
	if (game->counters[game->player] != 0){
		/* we start from the head and iter until arrive to the queue, oldxy is the new queue */
		while( game->arena[xy].xtra != 0b011){
				oldxy = xy;
				xy += tab_dxy[game->arena[xy].xtra&3];
		}

		/* remove (clear) the old queue and set the new queue */
		game->arena[xy].xtra = 0;
		game->arena[oldxy].xtra = 0b011;
	}
	/* increase counter */
	game->counters[game->player] = (uint8_t) ((game->counters[game->player]+1) % 10);
	/* next player */
	game->player = (uint8_t) !game->player;
}



/* find a random valid move */
t_move getRandomMove(t_game* game){
	t_xy hxy = game->heads[game->player];
	int score[4] = {0};
	/* test for all the directions */
	for(int d=0;d<4;d++)
	{
		/* check if the move is valid */
		if ( isValid(game, hxy, d)){
			score[d] = 1;
		}
	}
	/* find one random in the valid moves, if possible */
	if ((score[0]+score[1]+score[2]+score[3])==0)
		printf("No valid move....\n");

	return randomBest(score);
}


/* find a good valid move (only consider one round) */
t_move getOneRoundBestMove(t_game* game){
	static int nbC = 0;
	printf("nbC=%d\n",nbC++);
	t_xy hxy = game->heads[game->player];
	int score[4] = {0};
	t_game* gameT = (t_game*) malloc(sizeof(t_game));
	t_box* arena = (t_box*) malloc(sizeof(t_box)*game->sizeY*game->sizeX);
	/* test for all the directions */
	for(int d=0;d<4;d++)
	{
		/* check if the move is valid */
		if ( isValid(game, hxy, d)){
			/* copy the game */
			memcpy(gameT,game,sizeof(t_game));
			memcpy(arena,game->arena,sizeof(t_box)*game->sizeY*game->sizeX);
			gameT->arena = arena;
			/* play the move */
			playMove(gameT, d);
			/* evaluate it*/
			score[d] = scoreGame(gameT, hxy+tab_dxy[d]);
		}
	}
	/* no more need for them */
	free(arena);
	free(gameT);

	/* will we die ? */
	if ((score[0]+score[1]+score[2]+score[3])==0)
		sendComment("Good bye cruel world....");

	/* random among the best directions (direction with the highest score) */
	return randomBest(score);
}