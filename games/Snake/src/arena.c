#include "arena.h"
#include "stdlib.h"
#include "stdio.h"

#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

/* array of shift to apply on indexes xy to get the adjacent xy indexes in a given direction */
signed char tab_dxy[4] = {0};

/* debug */
void printxy(t_game* game, unsigned int xy){
printf("x=%d y=%d\n",xy%game->sizeX, xy/game->sizeX);
}

/* build the arena from the list of walls given by the server */
void buildGame(t_game* game, int* walls, int nbWalls, unsigned char sizeX, unsigned char sizeY){
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
}

/* get the queue of the snake, where head is the head position */
unsigned int getQueue(t_game* game, unsigned int head){
	/* we start from the head and iter until arrive to the queue */
	printf("Head:"); printxy(game, head);
	while( game->arena[head].xtra != 0b011)
			head += tab_dxy[game->arena[head].xtra];
	printf("Queue:"); printxy(game, head);
	return head;
}

/* play a move (update the game)
No need to check if the move is legal or not */
void playMove(t_game* game, t_move move){
	/* new head */
	unsigned int xy = game->heads[game->player];
	unsigned int oldxy = xy;
	unsigned int nh = xy + tab_dxy[move];
	printf("New head:"); printxy(game, nh);
	game->heads[game->player] = nh;
	game->arena[nh].p = game->player;
	game->arena[nh].xtra = 0b100 | ((move+2)&3);
	/* remove the queue (or not) */
	if (game->counters[game->player] != 0){
		/* we start from the head and iter until arrive to the queue */
		//while( game->arena[xy].xtra != 0b011){
		while( game->arena[xy].xtra > 3){
				oldxy = xy;
				xy += tab_dxy[game->arena[xy].xtra&3];
		}
		printf("Queue:"); printxy(game, xy);
		/* remove (clear) the old queue and set the new queue */
		game->arena[xy].xtra = 0;
		game->arena[oldxy].xtra = 0b011;
	}
	/* increase counter */
	game->counters[game->player]++;
	if (game->counters[game->player] == 10)
		game->counters[game->player] = 0;
	/* next player */
	game->player = ! game->player;
}


void displayArena(t_game* game){

	unsigned int xy=0;
	unsigned int x,y;
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
			char c =  game->arena[xy+x].xtra>=3 ? (game->arena[xy+x].p ? 'X' : 'Y') : ' ';
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

/* tire un nombre aléatoire entier entre a et b compris */
int randint(int a, int b)
{
	if (a==b)
		return a;
	int r = rand()%(b-a)+a;		/* BIAISED random !! */
	return r;
}

/* play a random move */
t_move getRandomMove(t_game* game){
	unsigned int hxy = game->heads[game->player];
	unsigned int nxy;
	int valid[4] = {0};
	int nbValid = 0;
	/* test for all the directions */
	for(int d=0;d<4;d++)
	{
		/* check if the move is valid */
		nxy = hxy + tab_dxy[d];
		if ( ( ! (game->arena[hxy].walls & (1<<d)) ) && (nxy < game->sizeX*game->sizeY) && (game->arena[nxy].xtra==0) ){
			valid[nbValid] = d;
			nbValid++;
		}
	}
	if (nbValid==0)
		printf("No valid move....\n");
	/* find one random in the valid moves */
	int d = randint(0,nbValid);
	return valid[d];
}