import numpy as np
import random

class Piece:
    def __init__(self, grid, center, letter, offset=(0, 0)):
        self.grid = grid
        self.center = center
        self.letter = letter
        self.width = grid.shape[0]
        self.offset = np.array(offset)

    # All of these transformations should modify the existing coordinates
    def rotate(self, direction="clockwise") -> None:
        """Rotates piece 90 degrees about the origin."""
        if self.letter == "O": pass
        if direction == "clockwise":
            self.grid = np.flip(self.grid.T, axis=1)
        elif direction == "counterclockwise":
            self.grid = (np.flip(self.grid, axis=1)).T
        else:
            raise ValueError("Invalid direction")

    def translate(self, direction) -> None:
        """Translates the piece one step in the given direction."""
        if direction == "left":
            self.offset[1] -= 1
        elif direction == "right":
            self.offset[1] += 1
        elif direction == "down":
            self.offset[0] += 1
        elif direction == "up":
            self.offset[0] -= 1
        else:
            raise ValueError("Invalid direction")
    
    def get_coords(self) -> np.ndarray:
        """Returns the coordinates of the piece."""
        coords = []
        for i in range(self.width):
            for j in range(self.width):
                if self.grid[i, j]:
                    coords.append((i + self.offset[0], j + self.offset[1]))
        return coords
    
    def get_row_strings(self) -> str:
        """Returns the piece as a list of strings representing each row."""
        return ["".join(["X" if c else " " for c in row]) for row in self.grid]

LETTERS = ["I", "O", "T", "S", "Z", "J", "L"]

GRID = {
    "I": np.array([
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ], dtype=int),
    "O": np.array([
        [1, 1,],
        [1, 1,],
    ], dtype=int),
    "T": np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0],
    ], dtype=int),
    "S":  np.array([
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0],
    ], dtype=int),
    "Z":  np.array([
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ], dtype=int),
    "J":  np.array([
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0],
    ], dtype=int),
    "L":  np.array([
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ], dtype=int),
}

CENTERS = {
    "I": np.array([1.5, 1.5]),
    "O": np.array([0.5, 0.5]),
    "T": np.array([1, 1]),
    "S": np.array([1, 1]),
    "Z": np.array([1, 1]),
    "J": np.array([1, 1]),
    "L": np.array([1, 1]),
}

def piece_from_letter(letter):
    """Creates a new piece corresponding to the provided letter."""
    return Piece(GRID[letter].copy(), CENTERS[letter].copy(), letter)

def random_piece():
    """Returns a random piece."""
    letter = random.choice(LETTERS)
    return piece_from_letter(letter)

