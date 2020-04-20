# CS50_AI
Course work for the CS50 Introduction to Artificial Intelligence

Each directory contains a coding project from Harvard's CS50 AI course (https://cs50.harvard.edu/ai/). Portions of the code were provided by the course, the rest was implemented by myself.

The projects belong to the following topics:

0. Search: Actors, TicTacToe
1. Knowledge: Knights, Minesweeper
2. Uncertainty: PageRank

...tbd...(work in progress)

***
Here are some descriptions and links for the individual projects:

ACTORS:

https://cs50.harvard.edu/ai/projects/0/degrees/

According to the Six Degrees of Kevin Bacon game, anyone in the Hollywood film industry can be connected to Kevin Bacon within six steps, where each step consists of finding a film that two actors both starred in. Here, I wrote a program that determines how many “degrees of separation” apart two actors are.

TICTACTOE:

https://cs50.harvard.edu/ai/projects/0/tictactoe/

Using a Minimax algorithm with Alpha Beta Pruning, I implemented an AI to play Tic-Tac-Toe optimally.

KNIGHTS:

https://cs50.harvard.edu/ai/projects/1/knights/

In a Knights and Knaves puzzle, the following information is given: Each character is either a knight or a knave. A knight will always tell the truth: if knight states a sentence, then that sentence is true. Conversely, a knave will always lie: if a knave states a sentence, then that sentence is false. The objective of the puzzle is, given a set of sentences spoken by each of the characters, determine, for each character, whether that character is a knight or a knave.

Here, I wrote a program that can solve such logical puzzles.

MINESWEEPER:

https://cs50.harvard.edu/ai/projects/1/minesweeper/

Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden “mines.” Clicking on a cell that contains a mine detonates the mine, and causes the user to lose the game. Clicking on a “safe” cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighboring cells – where a neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine.

Here, I implemented an intelligent agent to play Minesweeper optimally.

PAGERANK:

https://cs50.harvard.edu/ai/projects/2/pagerank/

When search engines like Google display search results, they do so by placing more “important” and higher-quality pages higher in the search results than less important pages. To determine a site's importance, the PageRank algorithm was created by Google’s co-founders. In PageRank’s algorithm, a website is more important if it is linked to by other important websites, and links from less important websites have their links weighted less. 

Here, I implement an AI to calculate PageRank in two variations.
