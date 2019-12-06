#ifndef __ARENA_H__
#define __ARENA_H__

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

typedef struct{
	unsigned char walls:4;
	unsigned char p:1;
	unsigned char xtra:3;
} t_box;

typedef struct{
	t_box* arena;    /* arena */
	unsigned char sizeX, sizeY;   /* its size */
	unsigned char counters[2];    /* counters 0 to 9, to know when we grow */
	unsigned char player;    /* who plays */
	unsigned int heads[2];  /* position of the head of the snakes */
} t_game;

/* build the arena from the list of walls given by the server */
void buildGame(t_game* game, int* walls, int nbWalls, unsigned char sizeX, unsigned char sizeY);

/* play a move (update the game) */
void playMove(t_game* game, t_move move);


void displayArena(t_game* game);

/* play a random move */
t_move getRandomMove(t_game* game);

#endif