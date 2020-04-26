import sys
import itertools
import random
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            for val in self.domains[var].copy():
                if len(val) != var.length:
                    self.domains[var].remove(val)

    def overlap_indices(self, x, y):
        """
        Returns the overlap positions in variables x and y, respectively.
        The first return value is the position of the overlapping letter in x,
        the second return value is the position of the overlapping letter in y.

        If there is no overlap, the function returns None, None.
        """
        if not self.crossword.overlaps[x, y]:
            return None, None

        # Determine the position of the overlap in x, y
        x_ind, y_ind = self.crossword.overlaps[x, y]
        return x_ind, y_ind

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Determine the position of the overlap in x, y
        x_ind, y_ind = self.overlap_indices(x, y)

        if x_ind is None:
            return False

        revision_made = False

        for x_val in self.domains[x].copy():
            consistent = False
            for y_val in self.domains[y]:
                if x_val[x_ind] == y_val[y_ind]:
                    consistent = True
                    break

            # This code will only be executed if for some word in x's domain,
            # there is no possible choice for y.
            if not consistent:
                self.domains[x].remove(x_val)
                revision_made = True

        return revision_made

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if not arcs:
            arcs = []
            for var1 in self.crossword.variables:
                for var2 in self.crossword.neighbors(var1):
                    arcs.append((var1, var2))

        while arcs:
            # Take first arc in queue and enforce (one-directional) arc consistency
            arc = arcs.pop(0)
            if self.revise(arc[0], arc[1]):
                if not self.domains[arc[0]]:
                    return False
                for var in self.crossword.neighbors(arc[0]):
                    if (var, arc[0]) not in arcs:
                        arcs.append((var, arc[0]))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return set(self.crossword.variables).issubset(set(assignment.keys()))

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Correct word lengths?
        for key, value in assignment.items():
            if len(value) != key.length:
                return False

        # All values distinct?
        if len(assignment) != len(set(assignment.values())):
            return False

        # All arcs consistent?
        for key1, value1 in assignment.items():
            for key2, value2 in assignment.items():
                if key1 == key2:
                    continue

                # Get positions of overlapping letters
                ind_1, ind_2 = self.overlap_indices(key1, key2)

                # Skip test if no overlap
                if ind_1 is None:
                    continue

                if value1[ind_1] != value2[ind_2]:
                    return False

        # Return True if none of the tests has failed
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domain = []
        for x_val in self.domains[var]:
            n_elim = 0
            for var2 in self.crossword.neighbors(var):
                if var2 not in assignment:
                    x_ind, y_ind = self.overlap_indices(var, var2)
                    x_letter = x_val[x_ind]
                    for y_val in self.domains[var2]:
                        if y_val[y_ind] != x_letter:
                            n_elim += 1
            domain += [(n_elim, x_val)]

        domain.sort()
        return [tup[1] for tup in domain]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Candidates are variables that are not yet assigned
        unassigned = list(self.crossword.variables.difference(set(assignment.keys())))

        # Get list of candidates together with their number of remaining variables.
        unassigned = [(len(self.domains[candidate]), candidate) for candidate in unassigned]

        # Return candidate with smallest number of remaining variables
        return min(unassigned, key=lambda tup: tup[0])[1]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.consistent(assignment):
            if self.assignment_complete(assignment):
                return assignment

            next_var = self.select_unassigned_variable(assignment)
            domain = self.order_domain_values(next_var, assignment)

            # Check domain values until valid solution is found
            while domain:
                next_val = domain.pop(0)
                new_assignment = assignment.copy()
                new_assignment[next_var] = next_val
                candidate = self.backtrack(new_assignment)
                if candidate:
                    return candidate

            return None
        else:
            return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
