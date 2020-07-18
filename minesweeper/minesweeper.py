import itertools
import random
from copy import deepcopy


class Minesweeper():
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


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        return self.mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        return self.safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            # Update sentence with the new information
            # Remove cell from sentence
            self.cells.remove(cell)
            self.count -= 1
            self.mines.add(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            # Update sentence with the new information
            # Remove cell from sentence
            self.cells.remove(cell)
            self.safes.add(cell)


class MinesweeperAI():
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

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.mark_safe(cell)

        # Add a new sentence to the AI's knowledge base
        sentence_cells = set()

        for i in [cell[0] - 1, cell[0], cell[0] + 1]:
            for j in [cell[1] - 1, cell[1], cell[1] + 1]:
                # Check if the cell is out of bounds
                if i < 0 or i >= self.width or j < 0 or j >= self.height:
                    continue
                # Check if the cell was already identified as a mine
                if (i, j) in self.mines:
                    count -= 1
                    continue
                # If the cell was not already identified as a mine or a
                # safe square, add it to sentence_cells
                if (i, j) not in self.safes:
                    sentence_cells.add((i, j))

        self.knowledge.append(Sentence(sentence_cells, count))

        # Based on the AI's knowledge base,
        # mark any possible additional cells as safe or as mines
        sentences_to_be_removed = []
        for sentence in self.knowledge:
            if sentence.count == 0:
                # There are no mines in this sentence
                # A copy of sentence.cells must be made
                # to be iterated through. Sentence.mark_safe()
                # modifies Sentence.cells, so it is not be possible
                # to call mark_safe in the same set we are iterating through.
                sacrificial_set = deepcopy(sentence.cells)
                for cell in sacrificial_set:
                    self.mark_safe(cell)
                sentences_to_be_removed.append(sentence)

            elif len(sentence.cells) == sentence.count:
                # All cells in this sentence are mines
                # A copy of sentence.cells must be made
                # to be iterated through. Sentence.mark_mine()
                # modifies Sentence.cells, so it is not be possible
                # to call mark_mine in the same set we are iterating through.
                sacrificial_set = deepcopy(sentence.cells)
                for cell in sacrificial_set:
                    self.mark_mine(cell)
                sentences_to_be_removed.append(sentence)

        # Remove marked sentences
        self.knowledge = [sentence for sentence in self.knowledge
                          if sentence not in sentences_to_be_removed]

        # Add new sentences to the AI's knowledge base
        # using the subset method
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1.cells != sentence2.cells:
                    # Check if the cells in sentence 2 are a subset
                    # of the cells in sentence 1
                    if sentence2.cells.issubset(sentence1.cells):
                        # A new sentence can be inferred
                        inferred_sentence = Sentence(sentence1.cells.difference(sentence2.cells),
                                                     sentence1.count - sentence2.count)

                        # Check if we can immediately identify
                        # the cells in the new sentence
                        if inferred_sentence.count == 0:
                            # There are no mines in this sentence:
                            for cell in inferred_sentence.cells:
                                self.mark_safe(cell)
                        elif len(inferred_sentence.cells) == inferred_sentence.count:
                            # All cells in this sentence are mines
                            for cell in inferred_sentence.cells:
                                self.mark_mine(cell)
                        else:
                            # If no cell could be identified,
                            # add the sentence to the knowledge base,
                            # if it's not already there
                            sentence_already_exists = False
                            for sentence in self.knowledge:
                                if inferred_sentence.cells == sentence.cells:
                                    sentence_already_exists = True
                                    break
                            if not sentence_already_exists:
                                self.knowledge.append(inferred_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = []
        for row in range(self.height):
            for column in range(self.width):
                if (row, column) not in self.moves_made:
                    if (row, column) not in self.mines:
                        possible_moves.append((row, column))

        if len(possible_moves) != 0:
            index = random.randint(0, len(possible_moves))
            return possible_moves[index]
        else:
            # There is no possible move to be made
            return None
