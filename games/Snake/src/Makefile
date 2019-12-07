# options
CC = gcc
CCFLAGS = -Wall
LDFLAGS = -lm

# fichiers du projet
SRC = clientAPI.c snakeAPI.c arena.c TH_test.c utils.c
OBJ = $(SRC:.c=.o)
EXEC = TH_test


# règle initiale
all: $(EXEC)

# règles de compilation
arena.o: arena.h
TH_test.o: arena.h
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