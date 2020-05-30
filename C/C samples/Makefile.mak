CC = gcc
CFLAGS = -g -Wall -Wshadow

RUN : Assignment_1.c
	$(CC) Assignment_1.c -o program $(CFLAGS)
test1 : RUN text1.txt
	./program < test1.txt