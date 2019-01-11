/*
* C program to randomly decide who I should
* play as in Tom Clancy's Rainbow Six Siege
* works for attackers and defenders
* current stats as of Aug.16/18
* August 2018
*/

#include <stdio.h>
#include <time.h>
#include <stdlib.h>

typedef struct op{
    int kills, deaths, wins, losses, killDeath, winLose;
    int opID;
    int ctuID;
    struct op *next;
}op;

int main(int argc, char **argv) {
	//code
	char *aTTKoperators[] = {"Sledge", "Thatcher", "Ash", "Thermite", "Twitch", "Montagne",
	                       "Glaz", "Fuse", "Blitz", "IQ", "Buck", "Blackbeard", "Capitao",
	                       "Hibana", "Jackal", "Ying", "Zofia", "Dokabei", "Finka", "Lion"};
	char *deFFoperators[] = {"Smoke", "Mute", "Castle", "Pulse", "Doc", "Rook", "Kapkhan",
	                       "Tachanka", "Jager", "Bandit", "Frost", "Valkyrie", "Caveira",
	                   	   "Echo", "Mira", "Lesion", "Ela", "Vigil", "Maestro", "Alibi"};
	char *ctus[] = {"SAS", "FBI", "GIGN", "SPETSNAZ", "GSG9", "JTF2", "NAVY SEALS", "BOPE",
	            "SAT", "GEO", "707th SMB", "SDU", "GROM", "CBRN Threat Unit", "GIS"};
	int arrATTK[2][20];
	int arrDEF[2][20];
	int a = 20, b = 20, c = 15;
	struct op temp;
	arrATTK[0][0] = 145;
	arrATTK[0][1] = 225;
	arrATTK[0][2] = 63;
	arrATTK[0][3] = 548;
	arrATTK[0][4] = 111;
	arrATTK[0][5] = 104;
	arrATTK[0][6] = 128;
	arrATTK[0][7] = 290;
	arrATTK[0][8] = 64;
	arrATTK[0][9] = 27;
	arrATTK[0][10] = 193;
	arrATTK[0][11] = 149;
	arrATTK[0][12] = 50;
	arrATTK[0][13] = 128;
	arrATTK[0][14] = 63;
	arrATTK[0][15] = 27;
	arrATTK[0][16] = 19;
	arrATTK[0][17] = 47;
	arrATTK[0][18] = 30;
	arrATTK[0][19] = 96;
	arrATTK[1][0] = 218;
	arrATTK[1][1] = 271;
	arrATTK[1][2] = 112;
	arrATTK[1][3] = 716;
	arrATTK[1][4] = 110;
	arrATTK[1][5] = 171;
	arrATTK[1][6] = 140;
	arrATTK[1][7] = 295;
	arrATTK[1][8] = 118;
	arrATTK[1][9] = 24;
	arrATTK[1][10] = 270;
	arrATTK[1][11] = 162;
	arrATTK[1][12] = 55;
	arrATTK[1][13] = 176;
	arrATTK[1][14] = 52;
	arrATTK[1][15] = 47;
	arrATTK[1][16] = 16;
	arrATTK[1][17] = 51;
	arrATTK[1][18] = 37;
	arrATTK[1][19] = 86;
	arrDEF[0][0] = 132;
	arrDEF[0][1] = 293;
	arrDEF[0][2] = 67;
	arrDEF[0][3] = 17;
	arrDEF[0][4] = 67;
	arrDEF[0][5] = 154;
	arrDEF[0][6] = 282;
	arrDEF[0][7] = 45;
	arrDEF[0][8] = 269;
	arrDEF[0][9] = 146;
	arrDEF[0][10] = 191;
	arrDEF[0][11] = 211;
	arrDEF[0][12] = 251;
	arrDEF[0][13] = 82;
	arrDEF[0][14] = 132;
	arrDEF[0][15] = 121;
	arrDEF[0][16] = 65;
	arrDEF[0][17] = 71;
	arrDEF[0][18] = 18;
	arrDEF[0][19] = 41;
	arrDEF[1][0] = 172;
	arrDEF[1][1] = 399;
	arrDEF[1][2] = 96;
	arrDEF[1][3] = 50;
	arrDEF[1][4] = 71;
	arrDEF[1][5] = 193;
	arrDEF[1][6] = 291;
	arrDEF[1][7] = 56;
	arrDEF[1][8] = 273;
	arrDEF[1][9] = 177;
	arrDEF[1][10] = 219;
	arrDEF[1][11] = 280;
	arrDEF[1][12] = 298;
	arrDEF[1][13] = 87;
	arrDEF[1][14] = 189;
	arrDEF[1][15] = 138;
	arrDEF[1][16] = 66;
	arrDEF[1][17] = 106;
	arrDEF[1][18] = 30;
	arrDEF[1][19] = 30;
	int j = 0;
	double num = 0, x= 0, y = 0;
	double attackDifferences[20];
	double defenceDifferences[20];
	for(int i = 0; i < 20; i++){
	    x = arrATTK[0][i];
	    y = arrATTK[1][i];
	    num =  x / y;
	    attackDifferences[i] = num;
	    x = arrDEF[0][i];
	    y = arrDEF[1][i];
	    num =  x / y;
	    defenceDifferences[i] = num;
	    
	}
	
	for(int i = 0; i < 20; i++){
	    printf("%s: \t\tkills: %d, deaths: %d, ratio: %f\n", aTTKoperators[i], arrATTK[0][i], arrATTK[1][i], attackDifferences[i]);
	}
	for(int i = 0; i < 20; i++){
	    printf("%s: \t\tkills: %d, deaths: %d, ratio: %f\n", deFFoperators[i], arrDEF[0][i], arrDEF[1][i], defenceDifferences[i]);
	}
	srand(time(NULL));
	int r = rand() % 20;
	/*while(r > 19 || r < 0){
	    r = rand() % 20;
	    printf("%d\n", r);
	}*/
	printf("\n\nEnter A for attack or D for defence\n");
	char choice;
	scanf("%c", &choice);
	printf("choice: %c\n", choice);
	printf("Random number: %d\n", r);
	if(choice != 'A' && choice != 'a' && choice != 'D' && choice != 'd'){
	    choice = 'A';
	}
	if(choice == 'a'){
	    choice = 'A';
	}
	else if(choice == 'd'){
	    choice = 'D';
	}
	if(choice == 'A'){
	    printf("Choose: ");
	    printf("%s\nKills: %d\tDeaths: %d\nRatio: %f\n", aTTKoperators[r], arrATTK[0][r], arrATTK[1][r], attackDifferences[r]);
	}
	else if(choice == 'D'){
	    printf("Choose: ");
	    printf("%s\nKills: %d\tDeaths: %d\nRatio: %f\n", deFFoperators[r], arrDEF[0][r], arrDEF[1][r], defenceDifferences[r]);
	}
	return 0;
}