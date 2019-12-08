#ifndef __UTILS_H__
#define __UTILS_H__

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "arena.h"


/* my pretty print (used for intern debug) */
void displayArena(t_game* game);

/* evalute the available surface */
int scoreGame(t_game* game, t_xy xy);

/* return 1 if a move from xy in direction d is valid */
int isValid(t_game* game, t_xy xy, int d);

/* debug printing */
void printxy(t_game* game, t_xy xy);

/* find a random index, among the indexes that gives the highest score */
int randomBest(int score[4]);

/* allocate data for the color and stack arrays */
void allocateUtilsArray(uint8_t sizeX, uint8_t sizeY);

/* free the color and stack arrays */
void freeUtilsArray();

#endif