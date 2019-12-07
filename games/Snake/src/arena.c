#include "arena.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>


#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

/* array of shift to apply on indexes xy to get the adjacent xy indexes in a given direction */
int8_t tab_dxy[4] = {0};
uint16_t *color;	/* array used to color, allocated once in buildGame, and free in freeGame */
t_xy *stack;	/* stack used to color */

/* debug printing */
void printxy(t_game* game, t_xy xy){
printf("x=%d y=%d\n",xy%game->sizeX, xy/game->sizeX);
}


/* find a random index, among the indexes that gives the highest score */
int randomBest(int score[4]){
	int start = rand();
	int highest = 0;
	/* we just look for the index with the highest score
	 * we don't care about equality, only the 1st is taken into account
	 * To add randomness, we just start from a random int (with (start+i)&3) */
	for(int i=0; i<4; i++){
		if (score[(start+i)&3]>score[highest])
			highest = (start+i)&3;
	}
	return highest;
}




/* build the arena from the list of walls given by the server */
void buildGame(t_game* game, int* walls, int nbWalls, uint8_t sizeX, uint8_t sizeY){
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
	game->heads[0] = 2 + sizeY/2*sizeX;
	game->heads[1] = sizeX - 3 + sizeY/2*sizeX;
	game->arena[game->heads[0]].xtra |= 0b011;  /* head of the snake */
	game->arena[game->heads[1]].p = 0;
	game->arena[game->heads[1]].xtra |= 0b011;  /* head of the snake */
	game->arena[game->heads[1]].p = 1;
	/* init the counters */
	game->counters[0] = game->counters[1] = 0;
	/* allocate data for the color array */
	color = (uint16_t*) malloc(sizeX*sizeY* sizeof(uint16_t));
	stack = (uint16_t*) malloc(sizeX*sizeY* sizeof(uint16_t));	/* TODO: probably 3*MAX(sizeX,sizeY) should be enough */
}


/* get the queue of the snake, where head is the head position */
unsigned int getQueue(t_game* game, t_xy head){
	/* we start from the head and iter until arrive to the queue */
	while( game->arena[head].xtra != 0b011)
			head += tab_dxy[game->arena[head].xtra];
	return head;
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
	game->arena[nh].xtra = 0b100 | ((move+2)&3);
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
	game->counters[game->player] = (game->counters[game->player]+1) % 10;
	/* next player */
	game->player = ! game->player;
}

/* my printing of Arena, to be sure my data are consistent */
void displayArena(t_game* game){

	t_xy xy=0;
	int x,y;
	for(y=0; y<game->sizeY; y++)
	{
		/* lignes Nord */
		printf("   ");
		for(x=0; x<game->sizeX; x++)
		{
			printf("+");
			printf( "%c", game->arena[xy+x].walls & NORTH ? '-' : ' ' );
		}
		printf("\n   ");
		/*lignes Ouest */
		for(x=0; x<game->sizeX; x++)
		{
			printf( "%c", game->arena[xy+x].walls&WEST ? '|' : ' ' );
			char c =  game->arena[xy+x].xtra>=3 ? (game->arena[xy+x].p ? 'X' : 'Y') : (color[xy+x]?'o':'.') ;
			printf( "%c", c);
		}
		/* ligne Est */
		printf( "%c\n", game->arena[xy+x-1].walls&EAST ? '|' : ' ' );
		xy += game->sizeX;
	}
	/* lignes Sud */
	xy -= game->sizeX;
	printf("   ");
	for( x=0; x<game->sizeX; x++)
	{
		printf("+");
		printf( "%c", game->arena[xy+x].walls&SOUTH ? '-' : ' ' );
	}
	printf("+\n");
}

/* return 1 if a move from xy in direction d is valid */
int isValid(t_game* game, t_xy xy, int d){
	t_xy nxy = xy + tab_dxy[d];
	return ( ! (game->arena[xy].walls & (1<<d)) ) && (nxy < game->sizeX*game->sizeY) && (game->arena[nxy].xtra==0);
}


/* play a random move */
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


/* evalute the available surface */
int scoreGame(t_game* game, t_xy xy){
	uint16_t score = 0;
	static uint16_t maxh = 0;
	t_xy nxy;
	/* reset the color array */
	memset(color, 0, sizeof(uint16_t)*game->sizeX*game->sizeY);
	/* head of the stack */
	uint16_t h = 1;
	stack[0] = xy;
	/* count how many cases are reachable */
	while(h>0){
		if (h>maxh)
			maxh = h;
		/* unstack */
		xy = stack[--h];
		color[xy] = 2;
		score++;
		/* stack the possibilities */
		for (int d = 0; d < 4; d++) {
			nxy = xy+tab_dxy[d];
			if ( isValid(game, xy, d) && (color[nxy] == 0) ){
				color[nxy] = 1;
				stack[h++] = nxy;
			}
		}
	}

	//displayArena(game);
	printf("\nMax h = %d\n", maxh);
	return score-1;


}

/* free the allocated memory */
void freeGame(t_game* game){
	free(game->arena);
	free(game);
	free(color);

}


/* play a move */
t_move bestMove(t_game* game){
	//static int nbC = 0;
	//printf("nbC=%d\n",nbC++);
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
	free(gameT->arena);
	free(gameT);

	/* will we die ? */
	if ((score[0]+score[1]+score[2]+score[3])==0)
		sendComment("Good bye cruel world....");

	/* random among the best directions (direction with the highest score) */
	return randomBest(score);
}