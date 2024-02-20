#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h> 
#define MAX_DIM 500
#define MIN_DIM 0
#define MAX_LEN 256
#define BLOCK_SIZE 16
#define SPACE 32
#define ENTER 10


struct board_square_t {
   int height;
   int width;
};

void generateName() {
    char firstname[MAX_LEN] = "1";
    char lastname[MAX_LEN] = "1";
    char fullname[MAX_LEN] = "";
    
    while(atoi(firstname) != 0){
        printf("\nPlease specify your first name: ");
        if(fgets(firstname, sizeof(firstname), stdin)){
            for (int i = 0; firstname[i] != '\0'; i++) { 
                if (isdigit(firstname[i])) { 
                    printf("\nThe string contains digit characters.\n"); 
                    strcpy(firstname, "1");
                    break;
                }
                if(firstname[i] == SPACE || firstname[0] == ENTER){
                    printf("\nThe string cannot contain neither white space nor enter.\n"); 
                    strcpy(firstname, "1");
                    break;
                }     
            } 
        }
    }

    while(atoi(lastname) != 0){ // continua quando nao tiver numeros
        printf("\nPlease specify your last name: ");
        if(fgets(lastname, sizeof(lastname), stdin)){
           for (int i = 0; lastname[i] != '\0'; i++) { 
                if (isdigit(lastname[i])) { 
                    printf("\nThe string contains digit characters.\n"); 
                    strcpy(lastname, "1");
                    break;
                }
                if(lastname[i] == SPACE || lastname[0] == ENTER){
                    printf("%c", lastname[0]);
                    printf("\nThe string cannot contain neither a white space nor enter.\n"); 
                    strcpy(lastname, "1");
                    break;
                }   
            }  
        }
    }

    strcat(fullname, firstname);
    strcat(fullname, lastname);

    printf("\nYour full name is: \n%s\n", fullname);
}


struct board_square_t* generateBoard(){
    int width = -1, height = -1, error = -1;
    char input[MAX_LEN] = "";
    struct board_square_t *board = NULL;

    while(width <= MIN_DIM || width > MAX_DIM){
        printf("\n\nPlease specify the board width[500 MAX]: \n");
        if(fgets(input, sizeof(input), stdin)){
            width = atoi(input);
            if(width == 0){
                printf("\nYou should provide a number, not a string!\n");
            }
        }
    }

    while(height <= MIN_DIM || height > MAX_DIM){
        printf("\n\nPlease specify the board height[500 MAX]: \n");
        if(fgets(input, sizeof(input), stdin)){
            height = atoi(input);
            if(height == 0){
                printf("\nYou should provide a number, not a string!\n");
            }
        }
    }

    board = (struct board_square_t*) malloc( width * height * sizeof(struct board_square_t));
    if(board == NULL){
        perror("Unable to allocate buffer");
        return NULL;
    }

    printf("\nBoard sucessfully generated with widht[%d] and height[%d]!\n\n", width, height);
    return board;
}

char* getBlock(int fd) {
    char* buf = (char*) malloc(BLOCK_SIZE); 

    if (!buf) {
        return NULL;
    }

    do{
        printf("\nWrite anything with 15 characters:\n");
    }
    while (read(fd, buf, BLOCK_SIZE) != BLOCK_SIZE);

    buf[BLOCK_SIZE] = '\0'; 
    return buf;
}


int main(int argc, char *argv[]){

    if (argc != 2) {
        printf("\nUsage: %s <name>\n", argv[0]);
        return 1;
    }

    printf("\nWelcome to the program %s! \n\n", argv[1]);

    struct board_square_t *board = generateBoard();
    free(board);

    generateName();
        
    printf("\nResult: %s\n", getBlock(0));

    return 0;
}