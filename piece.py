import numpy as np
import random

LETTERS = ["I", "O", "T", "S", "Z", "J", "L"]

class Piece:
    def __init__(self, grid: np.ndarray, center: np.ndarray, letter: str, offset: np.ndarray = np.zeros(2)):
        self.grid = grid
        assert grid.shape[0] == grid.shape[1], "Piece must be inside a square grid."
        self.width = grid.shape[0]
        self.center = center
        assert self.center.shape == (2,), "Center must be a 2D vector."
        self.letter = letter
        assert letter in LETTERS, "Invalid piece letter."
        self.offset = offset.astype(int)
        assert self.offset.shape == (2,), "Offset must be a 2D vector."

    # All of these transformations should modify the existing coordinates
    def rotate(self, direction: str = "clockwise") -> None:
        """Rotates piece 90 degrees about the origin."""
        if self.letter == "O": pass
        if direction == "clockwise":
            self.grid = np.flip(self.grid.T, axis=1)
        elif direction == "counterclockwise":
            self.grid = (np.flip(self.grid, axis=1)).T
        else:
            raise ValueError("Invalid direction")

    def translate(self, direction: str) -> None:
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

