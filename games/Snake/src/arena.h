#ifndef __ARENA_H__
#define __ARENA_H__

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "snakeAPI.h"

#define NORTH 1
#define EAST 2
#define SOUTH 4
#define WEST 8


/*  arena[0] is top left
	arena[sizeX] is top right
	arena[(sizeY-1)*sizeX] is bottom left
	arena[sizeY*sizeX-1] is bottom right
	arena[ y * sizeX + x] is (x,y) position */

typedef uint16_t t_xy;	/* used to store a position */

typedef struct{
	uint8_t walls:4;		/* walls, see NORTH, EAST, SOUTH and WEST */
	uint8_t p:1;			/* indicates which player is here, when there is a player */
	uint8_t xtra:3;			/* 0b000 when empty, 0b1dd when populates by a snake with direction dd to the next item of the snake
 							 * 0b011 when its the queue of the snake */
} t_box;

typedef struct{
	t_box* arena;    		/* arena (array of t_box) */
	uint8_t sizeX, sizeY;   /* its size */
	uint8_t counters[2];    /* counters 0 to 9, to know when we grow */
	uint8_t player;    		/* who plays (0 or 1) */
	t_xy heads[2];  		/* position of the head of the snakes */
} t_game;





/* build the arena from the list of walls given by the server */
void initGame(t_game *game, int *walls, int nbWalls, uint8_t sizeX, uint8_t sizeY);

/* free the allocated memory */
void freeGame(t_game* game);

/* play a move (update the game) */
void playMove(t_game* game, t_move move);


/* find a random valid move */
t_move getRandomMove(t_game* game);

/* find a good valid move (only consider one round) */
t_move getOneRoundBestMove(t_game* game);

#endif