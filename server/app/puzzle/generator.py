import random
import numpy as np

class CrosswordGenerator:
    def __init__(self, size=10):
        self.size = size
        self.grid = np.full((size, size), ' ', dtype=str)
        self.words = []

    def add_word(self, word, x, y, direction):
        """Attempts to place a word on the grid."""
        word = word.upper()
        if direction == "H":
            if y + len(word) > self.size:
                return False  # Out of bounds
            for i, letter in enumerate(word):
                if self.grid[x, y + i] not in (' ', letter):
                    return False  # Conflict
            for i, letter in enumerate(word):
                self.grid[x, y + i] = letter
        elif direction == "V":
            if x + len(word) > self.size:
                return False
            for i, letter in enumerate(word):
                if self.grid[x + i, y] not in (' ', letter):
                    return False
            for i, letter in enumerate(word):
                self.grid[x + i, y] = letter
        else:
            return False
        self.words.append((word, x, y, direction))
        return True

    def generate(self, words):
        """Fills the grid with given words randomly."""
        random.shuffle(words)
        for word in words:
            for _ in range(10):  # Try 10 random placements
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                direction = random.choice(["H", "V"])
                if self.add_word(word, x, y, direction):
                    break
        return self.grid

    def display(self):
        """Prints the crossword grid."""
        for row in self.grid:
            print(' '.join(row))

if __name__ == "__main__":
    words = ["PYTHON", "FASTAPI", "CROSSWORD", "PUZZLE"]
    crossword = CrosswordGenerator(size=10)
    crossword.generate(words)
    crossword.display()
