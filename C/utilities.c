#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// General utility functions for reading
// ints and strings (as whole lines).
//
// March 2020

int readInt() {
    int * x = malloc(sizeof (int));
    scanf("%d", x);
    return *x;
}


// Function to read in a string given a maxSize
// returns a pointer to the string in heap.
char * readString(int maxSize) {
    char arr[maxSize];
    char newlineScan[1];
    scanf("%c", newlineScan);
    scanf("%[^\n]", arr);
    int size = 0;
    char * ptr = arr;
    while(*(ptr + size) != 0 && size < maxSize) {
        size++;
    }
    char * res = malloc (sizeof (char) * size);
    char resArr[maxSize + 1];
    if (*newlineScan != '\n'){
        size++;
        strcpy(resArr, newlineScan);
        strcat(resArr, arr);
    }
    else {
        strcpy(resArr, arr);
    }
    for (int i = 0; i < size; i++) {
        *(res + i) = resArr[i];
    }
    return res;
}

int main() {
    int a, c, d, e, g, h;
    char * b, * f;
    a = readInt();
    b = readString(100);
    c = readInt();
    d = readInt();
    e = readInt();
    f = readString(100);
    g = readInt();
    h = readInt();
	printf("a: %d\nb: %s\nc: %d\nd: %d\ne: %d\nf: %s\ng: %d\nh: %d", a, b, c, d, e, f, g, h);
	return 0;
}
