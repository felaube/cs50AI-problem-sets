import sys

from crossword import Variable, Crossword
import math


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
        for var in self.domains:
            to_be_removed = set()
            for word in self.domains[var]:
                if len(word) != var.length:
                    to_be_removed.add(word)
            self.domains[var] -= to_be_removed

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        to_be_removed = set()
        overlaps = self.crossword.overlaps[x, y]
        if overlaps:
            for x_word in self.domains[x]:
                if not any(y_word[overlaps[1]] == x_word[overlaps[0]]
                           for y_word in self.domains[y]):
                    to_be_removed.add(x_word)
                    revised = True
        self.domains[x] -= to_be_removed

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            # Create initial queue
            arcs = []
            for var in self.crossword.variables:
                for neighbor in self.crossword.neighbors(var):
                    arcs.append((var, neighbor))

        while arcs:
            # Dequeue first element and enforce arc consistency
            (x, y) = arcs.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    # The domain for a variable is empty,
                    # hence, this crossword is impossible
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    # Queue new arcs
                    arcs.append((z, x))

        # Arc consistency was succesfully enforced for all variables
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment.keys():
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for variable in assignment:
            if len(assignment[variable]) != variable.length:
                return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = []
        n_values = []
        neighbors = self.crossword.neighbors(var)
        for word in self.domains[var]:
            n = 0
            for neighbor in neighbors:
                if neighbor in assignment:
                    # This neighbor already has a value assigned to it
                    continue
                overlaps = self.crossword.overlaps(var, neighbor)
                for neigh_word in self.domains[neighbor]:
                    if word[overlaps[0]] != neigh_word[overlaps[1]]:
                        n += 1
            # If that's the first word, just add it to the list
            if not values:
                values.append(word)
                n_values.append(n)
            else:
                # Look for the right index, where the word should be inserted
                list_modified = False
                for index, num in enumerate(n_values):
                    if n < num:
                        list_modified = True
                        n_values.insert(index, n)
                        values.insert(index, word)
                        break
                if not list_modified:
                    values.append(word)
                    n_values.append(n)

        return values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Initialize variables
        chosen_var = None
        chosen_n = math.inf
        chosen_degree = 0

        # Check every possible variable
        for var in self.crossword.variables:
            # Skip already assigned variables
            if var in assignment:
                continue
            # Choose variable with the minimum number of remaining values
            # in its domain
            n_values = len(self.domains[var])
            if n_values < chosen_n:
                chosen_var = var
                chosen_n = n_values
                chosen_degree = len(self.crossword.neighbors(var))
            # If tied, choose the one with the largest degree
            elif n_values == chosen_n:
                degree = len(self.crossword.neighbors(var))
                if degree > chosen_degree:
                    chosen_var = var
                    chosen_n = n_values
                    chosen_degree = degree

        return chosen_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)

        for value in self.domains[var]:
            if self.consistent(assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result:
                    return result
            assignment.pop(var)
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
