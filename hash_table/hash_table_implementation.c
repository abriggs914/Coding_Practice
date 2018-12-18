#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// #define size 93

int numCollisions = 0, numUnused = 0, size, hfVal;
int * ar;

typedef struct node{
    int data;
    struct node * next;
};

// struct node * root;
struct node ** arr;

int hash(int n){
    int a = pow((n+n),2);
    int b = pow((n-1),2);
    // printf("a: %d, b: %d\n",a,b);
    if(b == 0){
        b++;
    }
    if(n < 0){
        n = -1*n;
    }
    return n % hfVal;
}

int genArray() {
    scanf("%d %d",&size,&hfVal);
    // size = 17;
    // hfVal = 11;
    arr = malloc(size*sizeof(struct node*));
    ar = malloc(hfVal*sizeof(int));
	//code
	int x, y;
	printf("{");
	for(int i = 0; i < size; i++){
	    x = rand();
	    if(((x - (x/2)) % 2) == 0){
	        x = -1*x;
	    }
	    x = x % hfVal;
	    if(i < size - 1){
	        printf("%d,", x);
	    }
	    else{
	        printf("%d", x);
	    }
	    ar[i] = x;
	}
	printf("}\n");
	return 0;
}

void insert(int h, struct node * temp){
    if(arr[h] == NULL){
        arr[h] = temp;
    }
    else{
        numCollisions++;
        struct node * t = arr[h];
        while(t->next != NULL){
            t = t->next;
        }
        t->next = temp;
    }
}

int main() {
	//code
	int i,h;
// 	size = 5;
// 	int ar[] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50};
// 	int ar[] = {-1383,886,777,-915,1793,-335,1386,-492,649,1421,362,-27,690,-59,-1763,1926,-540,1426,-1172,-1736,-1211,-1368,-567,429,1782,1530,862,-1123,-67,-1135,1929,1802,22,1058,1069,-167,1393,-456,-1011,42,229,1373,421,-919,-1784,537,1198,-324,-315,370,413,1526,-91,-980,-1956,1873,862,1170,-996,1281,305,925,-1084,-327,-336,505,846,1729,1313,1857,-124,-1895,1582,545,814,-1367,1434,-364,-43,1750,-1087,-808,-1276,1178,-1788,-1584,-1403,-651,754,-399,-1932,-1060,-1676};
    genArray();
	for(i = 0; i < size; i++){
	   struct node * temp = malloc(sizeof(struct node));
	   temp->data = ar[i];
	   //printf("temp->data: %d\n", temp->data);
	   h = hash(ar[i]);
	   temp->next = NULL;
	   insert(h, temp);
	   // printf("temp->data: %d ", temp->data);
	   
	   //arr[i] = temp;
	}
	
	for(i = 0; i < size; i++){
	    if(arr[i] == NULL){
	        continue;
	    }
	    while(arr[i] != NULL){
	        printf("{arr[%d]->data: %d} -> ",i,arr[i]->data);
	        arr[i] = arr[i]->next;
	    }
	    printf("NULL\n");
	}
	numUnused = numCollisions;
	printf("\n\tTotal Collisions: %d, Unused cells: %d, out of size: %d\n",numCollisions,numUnused,size);
	return 0;
}