import random
import sqlite3

GRID_SIZE = 12

class WordPlacement:
    def __init__(self, word, clue, x, y, direction):
        self.word = word
        self.clue = clue
        self.x = x
        self.y = y
        self.direction = direction  # "across" or "down"

    def to_dict(self):
        return {
            "word": self.word,
            "clue": self.clue,
            "x": self.x,
            "y": self.y,
            "dir": self.direction
        }

def fetch_clues(source, db_path="app/db/news.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT clue, word FROM clues WHERE source = ?", (source,))
    clues = cur.fetchall()
    conn.close()
    return [{"clue": c, "word": a.upper()} for c, a in clues if a.isalpha()]

def generate_crossword(clues, grid_size=GRID_SIZE):
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    placed_words = []

    random.shuffle(clues)
    clues.sort(key=lambda x: -len(x["word"])) 

    for index, entry in enumerate(clues):
        word = entry["word"]
        clue = entry["clue"]
        candidates = []

        if index == 0:
            # First word: place at top-left (1,1), horizontal
            if len(word) <= grid_size:
                for i, letter in enumerate(word):
                    grid[1][i+1] = letter
                placed_words.append(WordPlacement(word, clue, 1, 1, "across"))
            continue

        # Try to find intersecting positions, or place randomly if no intersection
        for placed in placed_words:
            for i, l1 in enumerate(placed.word):
                for j, l2 in enumerate(word):
                    if l1 == l2:
                        # Try to place new word crossing this one
                        if placed.direction == "across":
                            x = placed.x + i
                            y = placed.y - j
                            if is_valid_position(grid, word, x, y, "down"):
                                candidates.append((x, y, "down"))
                        else:
                            x = placed.x - j
                            y = placed.y + i
                            if is_valid_position(grid, word, x, y, "across"):
                                candidates.append((x, y, "across"))

        # If no intersecting positions were found, try random placement
        if not candidates:
            for _ in range(100):  # Limit retry attempts to avoid infinite loops
                x = random.randint(0, grid_size - 1)
                y = random.randint(0, grid_size - 1)
                direction = random.choice(["across", "down"])
                if is_valid_position(grid, word, x, y, direction):
                    candidates.append((x, y, direction))
                    break

        if candidates:
            best = candidates[0]  # In this case, just use the first valid position
            x, y, direction = best
            place_word(grid, word, x, y, direction)
            placed_words.append(WordPlacement(word, clue, x, y, direction))

    return {
        "grid": grid,
        "words": [w.to_dict() for w in placed_words]
    }

def is_valid_position(grid, word, x, y, direction):
    try:
        for i in range(len(word)):
            gx, gy = (x + i, y) if direction == "down" else (x, y + i)
            if gx < 0 or gy < 0 or gx >= GRID_SIZE or gy >= GRID_SIZE:
                return False
            if grid[gx][gy] != "." and grid[gx][gy] != word[i]:
                return False
            # If intersecting with another word, ensure no conflict
            if grid[gx][gy] != "." and grid[gx][gy] != word[i]:
                return False
        return True
    except IndexError:
        return False


def count_crosses(grid, word, x, y, direction):
    count = 0
    for i in range(len(word)):
        gx, gy = (x + i, y) if direction == "down" else (x, y + i)
        if grid[gx][gy] == word[i]:
            count += 1
    return count

def place_word(grid, word, x, y, direction):
    for i in range(len(word)):
        gx, gy = (x + i, y) if direction == "down" else (x, y + i)
        grid[gx][gy] = word[i]
