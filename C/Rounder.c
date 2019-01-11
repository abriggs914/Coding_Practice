#include <stdio.h>
#include <stdlib.h>

int roundUp(int n);
int roundDown(int n);

int main() {
	//code
	int a, b, c =0,d;
	while(c < 4){
    	scanf("%d", &a);
    	b = roundUp(a);
    	printf("UP: %d, %d\n",a, b);
    	d = roundDown(a);
    	printf("DOWN: %d, %d\n",a, d);
    	if((b+d) != 100 && (a%100) != 0){
    	    printf("ERROR\n");
    	}
    	c++;
	}
    	return 0;
}

int roundUp(int n){
    int c = 0, d = 0;
    if(n%100 > 0)
        c = (n/100+1)*100;
    else
        return 0;
    return c-n;
}

int roundDown(int n){
    int c = 0, d = 0;
    if(n%100 > 0)
        c = n%100;
    else
        return 0;
    return c;
}