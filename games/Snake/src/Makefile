# options
CC = gcc
CCFLAGS = -Wall
LDFLAGS = -lm

# fichiers du projet
SRC = Q1.c clientAPI.c snakeAPI.c
OBJ = $(SRC:.c=.o)
EXEC = Q1


# règle initiale
all: $(EXEC)

# règles de compilation
%.o: %.c
	$(CC) $(CCFLAGS) -o $@ -c $<
	
# règles d'édition de liens
$(EXEC): $(OBJ)
	$(CC) -o $@ $^ $(LIBS) $(LDFLAGS)

# règles supplémentaires
clean:
	rm -f *.o
rmproper:
	rm -f $(EXEC) *.o