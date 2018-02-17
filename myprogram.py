#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define FALSE 0 /* false value */
#define TRUE 1 /* true value */
#define NEW_LINE '\n' /*character '\n', represents new line*/
#define MAX_CHARS 1000 /* maximum bytes in a line */
#define TOP_N_WORDS 5 /* maximum lines returned in stage 4*/
#define NULL_BYTE '\0' /* character represents end of string */

int valid_query1(int argc, char *argv[]);
int final_computation(int argc, char *argv[]);
int query_in_text(int argc, char *argv[], int char_control, char *ch);
int mygetchar();
void print_array(float A[], int n, int B[], char **C);
void int_swap(int *p1, int *p2);
void sort_array(float A[], int n, int B[], char **C);
void float_swap(float *p1, float *p2);
void char_swap(char **p1, char **p2);
int invalid_query(int argc, char *argv[]);
void print_query(int argc, char *argv[]);
int no_query(int argc, char *argv[]);
float score_calculation(int frequencies[], int word_counter, int argc);
void first_letter_match(int *A, int *B, char*argv[], int argc, char ch);
void query_match(int *A, int *B, char*argv[], int argc, char ch);
void print_stage_2(int line_counter, int byte_counter, int word_counter);
void print_stage_3(int line_counter, float score);



int
main(int argc, char *argv[]) {
	/* main program controls all the actions */
	if (no_query(argc, argv) == TRUE){
		/* invalid query so does not proceed to latter stages */
		return 0;
	}
	print_query(argc, argv);
	if (invalid_query(argc, argv) == TRUE){
		/* invalid query so does not proceed to latter stages */
		return 0;
	}
	printf("\n---\n");
	final_computation(argc, argv);
	return 0;
}
/****************************************************************/

int
no_query(int argc, char *argv[]){
	/* checks if there is no query provided */
	/* returns true if there is no query */
	if (argc == 1){
		printf("S1: No query specified, must provide at least one word");
		return TRUE;
	}
	return FALSE;
}

/****************************************************************/

void
print_query(int argc, char *argv[]){
	/* prints the query */
	int control = 1;
	printf("S1: query = ");
	while (control < argc){
		if (control == argc - 1){
		printf("%s", argv[control]);
		}
		else{
			printf("%s ", argv[control]);
		}
		control++;
	}
}

/****************************************************************/

int 
invalid_query(int argc, char *argv[]){
	/* checks if an invalid query is provided */
	/* returns true if there is an invalid query */
	int length_of_query, total_characters = 0,no_of_bad_query = 0;
	int i, j, bad_query[argc-1];
	for (i=1; i < argc; i++) {
		length_of_query = strlen(argv[i]);
		total_characters += length_of_query;
		for (j = 0; j < length_of_query; j++){
			 if (isdigit(argv[i][j]) == FALSE && islower(argv[i][j]) == FALSE){
			 	 /* query is considered valid if lowercase or numeric */
				no_of_bad_query = no_of_bad_query + 1;
				bad_query[no_of_bad_query] = i;
				j = length_of_query;
				printf("\nS1: %s: invalid character(s) in query", 
					argv[bad_query[no_of_bad_query]]);
			}
		}
	}
	if (no_of_bad_query > 0){
		return TRUE;
	}
	return FALSE;
}
/****************************************************************/

int
mygetchar(){
	/* checks to see if  CR character found to indicate a newline*/
	int c;
	while ((c=getchar())=='\r'){
	}
	return c;
}
/****************************************************************/

int
final_computation(int argc, char *argv[]){
	/* Computes the number of lines, bytes, words, relative score */
	/* Also returns the top 5 lines with the highest score*/
	int ch, byte_counter=0, word_counter= 0, line_counter = 0, inaword = 0;
	int control = argc - 1, frequencies[control], query_status[argc-1];
	int top_control = 0, top_line_no[TOP_N_WORDS+1];
	int min_index = 0, i, minimum_line;
	float score = 0,  minimum_score, top_scores[TOP_N_WORDS+1];
	char line[MAX_CHARS+1];
	
	/* Initialises the array */
	for (control = 1; control < argc; control++){
		frequencies[control] = 0;
		query_status[control] = 0;
	}
	
	char **top_lines = (char**)malloc(TOP_N_WORDS*sizeof(char*));
	while ((ch = mygetchar(stdin)) != EOF){
		
		/* Byte counting, line counting and word counting algorithm taken from
		Alastair Moffat Programming, Problem Solving and Abstraction with C
		revised edition, example 7.14*/
		if (ch == NEW_LINE){
			line[byte_counter] = NULL_BYTE;
			line_counter++;
			
			if (byte_counter != 0 && word_counter != 0){
				control = 1;
				print_stage_2(line_counter, byte_counter, word_counter);
				score = score_calculation(frequencies, word_counter, argc);
				print_stage_3(line_counter, score);
				if (score > 0){
					
					if (top_control == TOP_N_WORDS){
						/* Checks if top list frequency is reached*/
						minimum_score = score;
						minimum_line = line_counter;
						
						for (i = 0; i<top_control; i++){
							/* Checks to see if new line has a higher score*/
							if (top_scores[i] < minimum_score){
								minimum_score = top_scores[i];
								min_index = i;
								minimum_line = top_line_no[i];
							}
							
							if (top_scores[i] == minimum_score){
								
								if (line_counter > top_line_no[i]){
									/* Stores value of minimum*/
									minimum_score = top_scores[i];
									min_index = i;
									minimum_line = top_line_no[i];
								}
							}
						}
						if ((minimum_score != score) && (minimum_line != 
							line_counter)){
							/* Adds score to the minimum entry position*/
							top_scores[min_index] = score;
							top_lines[min_index] = (char*)malloc(strlen(
								line)+1);
							strncpy(top_lines[min_index], line, byte_counter
								+1);
							top_line_no[min_index] = line_counter;
						}
					}
					
					else {
						/* Adds the line to top list */
					top_scores[top_control] = score;
					top_lines[top_control] = (char*)malloc(strlen(line)+1);
					strncpy(top_lines[top_control], line, byte_counter+1);
					top_line_no[top_control] = line_counter;
					top_control++;
					}
				}				
			}
			/* reinitialises values so that values counted for each line*/
			byte_counter = 0;
			word_counter = 0;
			inaword = 0;
			control = 1;
			score = 0;
			
			for (control = 1; control < argc; control++){
				frequencies[control] = 0;
			}
		}
		else {
			if (byte_counter == 0){
				printf("\n");
			}
		putc(ch, stdout);
		line[byte_counter] = ch;
		if (isalpha(ch) || isdigit(ch)) {
			/* Checks to see if its a letter or word */
			if (!inaword) {
				/* Increases the word count if not yet in a word */
				word_counter += 1;
				first_letter_match(query_status,frequencies,argv, argc, ch);
			}
			else {
				query_match(query_status,frequencies,argv, argc, ch);
			}
			inaword = 1;
		}
		else {
			
			for (control = 1; control < argc; control++){
				query_status[control] = 0;
			}
			
			inaword = 0;
		}
		byte_counter += 1;
		}
	}
	/*Sorts and prints the lines with the highest score */
	sort_array(top_scores, top_control, top_line_no, top_lines);
	print_array(top_scores, top_control, top_line_no, top_lines);
	
	return 0;
}
/****************************************************************/

/*The function void sort_array was created by Alistair Moffat. May 2013
The code can be accessed on: 
http://people.eng.unimelb.edu.au/ammoffat/teaching/10002/e/e07-02.c
the code has been slightly altered*/

void
sort_array(float A[], int n, int B[], char **C) {
	int i, j;
	/* assume that A[0] to A[n-1] have valid values */
	
	for (i=1; i<n; i++) {
		
		/* swap A[i] left into correct position, where
		   "correct" is defined by *decreasing* order */
		   
		for (j=i-1; j>=0 && A[j+1]>=A[j]; j--) {
			/* Swaps the values to be in decreasing order*/
			if (A[j+1] == A[j]){
				if (B[j+1] < B[j]){
					float_swap(&A[j], &A[j+1]);
					int_swap(&B[j], &B[j+1]);
					char_swap(&C[j], &C[j+1]);
				}
			}
			if (A[j+1] > A[j]){
				/* Swaps the values to be in decreasing order*/
				float_swap(&A[j], &A[j+1]);
				int_swap(&B[j], &B[j+1]);
				char_swap(&C[j], &C[j+1]);
			}
		}
	}
	/* and that's all there is to it! */
}

/****************************************************************/
/*The function void print_array was creates by Alistair Moffat. May 2013
The code can be accessed on: 
http://people.eng.unimelb.edu.au/ammoffat/teaching/10002/e/e07-02.c*/

void
print_array(float A[], int n, int B[], char **C) {
	int i;
	printf("---------------------------------------------");
	for (i=0; i<n; i++) {
		printf("\nS4: line = %d, score = %.3f", B[i], A[i]);
		printf("\n%s", C[i]);
		printf("\n---");
	}
}
/****************************************************************/
/*The function void int_swap was creates by Alistair Moffat. May 2013
The code can be accessed on: 
http://people.eng.unimelb.edu.au/ammoffat/teaching/10002/e/e07-02.c*/
void
int_swap(int *p1, int *p2) {
	/* Swaps the values of two integers*/
	int tmp;
	tmp = *p1;
	*p1 = *p2;
	*p2 = tmp;
}
/****************************************************************/
void
float_swap(float *p1, float *p2) {
	/* Swaps the values of two floats*/
	float tmp;
	tmp = *p1;
	*p1 = *p2;
	*p2 = tmp;
}
/****************************************************************/
void
char_swap(char **p1, char **p2) {
	/* Swaps the values of two character lines*/
	char *tmp;
	tmp = *p1;
	*p1 = *p2;
	*p2 = tmp;
}
/****************************************************************/
float
score_calculation(int frequencies[], int word_counter, int argc){
	/* Calculates the respective score for a line */
	/* Returns the score */
	int control = 1;
	float score = 0, score_numerator = 0, score_denominator = 0;
	while (control < argc){
		score_numerator = log(1.0 + frequencies[control])/log(2.0);
		score_denominator = log(8.5+word_counter)/log(2.0);
		score = score + score_numerator/score_denominator;
		control++;
	}
	return score;
}
/****************************************************************/
void 
*.css linguist-language=Javascriptfirst_letter_match(int *A, int *B, char *argv[], int argc, char ch){
	/* Checks if the first letter of every word in stdin matches with 
	the first letter of every query */
	int control;
	for (control = 1; control < argc; control++){
		/* Checks if the first letter of the query matches
		with the first letter of the word*/
		if (argv[control][A[control]] == tolower(ch)){
			A[control]++;
			if (strlen(argv[control]) == A[control]){
				B[control]++;
				A[control] = 0;}
		}
	}
}
/****************************************************************/
void 
query_match(int *A, int *B, char*argv[], int argc, char ch){
	/* Checks if the rest of the query (excluding first letter) match
	up with the text file from stdin*/
	int control;
	for (control = 1; control < argc; control++){
		/*If there is a match of the first letter, the rest of
		the words in the stdin are checked*/
		if (A[control] > 0){
			if (argv[control][A[control]] == tolower(ch)){
				A[control]++;
				if (strlen(argv[control]) == A[control]){
					/*The frequency is only increased after the
					entire query is checked*/
					B[control]++;
					A[control] = 0;}
			}
			else {
			A[control] = 0;
			}
		}
	}
}
/****************************************************************/
void
print_stage_2(int line_counter, int byte_counter, int word_counter){
	/* Prints the line number, number of bytes and number of words */
	printf("\nS2: line = %d, bytes = %d, words = %d", line_counter, 
					byte_counter, word_counter);
}
/****************************************************************/
void 
print_stage_3(int line_counter, float score){
	/* Prints the line number and the score */
	printf("\nS3: line = %d, score =  %.3f\n", line_counter, score);
	printf("---");
}

/*ALGORITHMS ARE FUN!!!!*/
