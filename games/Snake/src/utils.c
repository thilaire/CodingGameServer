#include "utils.h"

/* array of shift to apply on indexes xy to get the adjacent xy indexes in a given direction */
extern int8_t tab_dxy[4];
uint8_t *color;			/* array used to colorize the arena (see what is reachable or not) */
t_xy *stack;			/* stack used to colorize */

/* allocate data for the color and stack arrays */
void allocateUtilsArray(uint8_t sizeX, uint8_t sizeY){
	color = (uint8_t*) malloc(sizeX*sizeY* sizeof(uint8_t));
	stack = (t_xy*) malloc(sizeX*sizeY* sizeof(t_xy));	/* TODO: probably sizeX*sizeY/3 should be enough */
}

/* free the color and stack arrays */
void freeUtilsArray(){
	free(color);
	free(stack);
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
			char c =  (char) (game->arena[xy+x].xtra>=3 ? (game->arena[xy+x].p ? 'X' : 'Y') : (color[xy+x]?'o':'.'));
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



/* evalute the available surface */
int scoreGame(t_game* game, t_xy xy){
	uint16_t score = 0;
	static uint16_t maxh = 0;
	t_xy nxy;
	/* reset the color array */
	memset(color, 0, sizeof(uint8_t)*game->sizeX*game->sizeY);
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
	//printf("\nMax h = %d\n (ratio=%f)\n", maxh, game->sizeX*game->sizeY/(double)maxh);
	return score-1;
}

/* return 1 if a move from xy in direction d is valid */
int isValid(t_game* game, t_xy xy, int d){
	t_xy nxy = xy + tab_dxy[d];
	return ( ! (game->arena[xy].walls & (1<<d)) ) && (nxy < game->sizeX*game->sizeY) && (game->arena[nxy].xtra==0);
}


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