import itertools
import random
from random import choice
from copy import deepcopy


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self, known_safes):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If all safe locations in the Sentence are known,
        # the other cells must be mines.
        # This is the case if the Sentence counter is equal to the
        # number of Sentence cells not known to be safe.

        safes_in_sentence = known_safes.intersection(self.cells)

        if self.count == len(self.cells) - len(safes_in_sentence):
            return self.cells.difference(safes_in_sentence)
        return set()

    def known_safes(self, known_mines):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If all mine locations in the sentence are known,
        # the other cells must be safe.
        # This is the case if the Sentence's mine counter is equal to the
        # number of Sentence cells that are in the set of known mines.

        mines_in_sentence = known_mines.intersection(self.cells)

        if self.count == len(mines_in_sentence):
            return self.cells.difference(mines_in_sentence)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            # delete sentence with empty cells
            if not sentence.cells:
                self.knowledge.remove(sentence)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            # delete sentence with empty cells
            if not sentence.cells:
                self.knowledge.remove(sentence)

    def update_knowledge_base(self):
        """
        Mark any additional cells as safe or as mine if it can be concluded based on the AI's knowledge base
        """
        for sentence in self.knowledge:
            for safe_cell in sentence.known_safes(self.mines):
                self.mark_safe(safe_cell)

            for mine in sentence.known_mines(self.safes):
                self.mark_mine(mine)

    def infer_new_sentences(self):
        """
        Add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        """
        for sentence_1 in deepcopy(self.knowledge):
            # Prevent comparing a sentence with itself
            knowledge_without_s1 = deepcopy(self.knowledge)
            knowledge_without_s1.remove(sentence_1)
            for sentence_2 in knowledge_without_s1:

                # Any time we have two sentences set1 = count1 and set2 = count2
                # where set2 is a subset of set1, then we can construct
                # the new sentence set1 - set2 = count1 - count2
                if sentence_2.cells.issubset(sentence_1.cells):
                    new_sentence_cells = sentence_1.cells.difference(sentence_2.cells)
                    new_sentence_count = sentence_1.count - sentence_2.count
                    new_sentence = Sentence(new_sentence_cells, new_sentence_count)
                    # Avoid duplicate sentences in knowledge base
                    if new_sentence not in self.knowledge:
                        self.knowledge.append(new_sentence)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """
        # mark the cell as a move that has been made
        self.moves_made.add(cell)

        # mark the cell as safe
        self.mark_safe(cell)

        # add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        new_sentence_cells = []

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Add cell to new sentence if in bounds and not already played
                if 0 <= i < self.height and 0 <= j < self.width:

                    if (i, j) not in self.moves_made:
                        new_sentence_cells.append((i, j))

        # Only add sentence if cells are not empty
        if new_sentence_cells:
            new_sentence = Sentence(new_sentence_cells, count)
            self.knowledge.append(new_sentence)

        # Update knowledge base and infer new sentences iteratively until nothing new can be learned
        new_knowledge_gained = True
        new_mines_identified = True
        new_safes_identified = True

        while new_knowledge_gained or new_mines_identified or new_safes_identified:
            old_knowledge = len(self.knowledge)
            num_mines_old = len(self.mines)
            num_safes_old = len(self.safes)

            # Mark any additional cells as safe or as mine if it can be concluded based on the AI's knowledge base
            self.update_knowledge_base()

            # Add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
            self.infer_new_sentences()

            new_knowledge_gained = old_knowledge != len(self.knowledge)
            new_mines_identified = num_mines_old != len(self.mines)
            new_safes_identified = num_safes_old != len(self.safes)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) > len(self.moves_made):
            return choice(tuple(self.safes.difference(self.moves_made)))

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        candidates = set()
        for i in range(self.height - 1):
            for j in range(self.width - 1):
                if ((i, j) not in self.moves_made) and ((i, j) not in self.mines):
                    candidates.add((i, j))

        if not candidates:
            return None

        return choice(tuple(candidates))
