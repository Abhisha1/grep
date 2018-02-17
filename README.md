# grep
Serves a similar function as grep on C through finding the matching words in a given function.
Initially, it checks the command line for an argument/query. If there is some query provided, it proceeds to check if that query is present in the given file. It must check each line for the query and compute each line with an associated score. Then, the final output must be a ranked summary output displaying the lines with the highest score first (based on the score), also displaying the line from the input file and with the line number.


