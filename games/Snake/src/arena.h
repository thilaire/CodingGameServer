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

typedef uint16_t t_xy;

typedef struct{
	uint8_t walls:4;
	uint8_t p:1;
	uint8_t xtra:3;
} t_box;

typedef struct{
	t_box* arena;    /* arena */
	uint8_t sizeX, sizeY;   /* its size */
	uint8_t counters[2];    /* counters 0 to 9, to know when we grow */
	uint8_t player;    /* who plays */
	t_xy heads[2];  /* position of the head of the snakes */
} t_game;

/* build the arena from the list of walls given by the server */
void buildGame(t_game* game, int* walls, int nbWalls, uint8_t sizeX, uint8_t sizeY);

/* play a move (update the game) */
void playMove(t_game* game, t_move move);


void displayArena(t_game* game);

/* play a random move */
t_move getRandomMove(t_game* game);

/* evalute the available surface */
int score(t_game* game, t_xy xy);

/* free the allocated memory */
void freeGame(t_game* game);

/* return 1 if a move from xy in direction d is valid */
int isValid(t_game* game, t_xy xy, int d);

t_move bestMove(t_game* game);

#endif