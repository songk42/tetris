import numpy as np
import piece

class Board:
    def __init__(self, width=10, height=20):
        # TODO: height vs. print height? how will pieces spawn
        self.width = width
        self.height = height
        # (0, 0) is the top left corner of the board
        self.grid = np.array([[" " for _ in range(width)]] * height)
        self.piece = None
        self.new_piece = False
        self.add_piece(piece.random_piece())
        self.game_over = False

    def reset_grid(self) -> None:
        self.grid = np.array([[" " for _ in range(self.width)] * self.height])
    
    def add_piece(self, piece) -> None:
        self.piece = piece
        self.new_piece = False
        while max([i for (i, _) in self.piece.get_coords()]) >= self.height:
            self.move("down")
        if self.check_collision() == 2:
            self.game_over = True
        self.set_piece()

    def step(self) -> None:
        """Move the current piece one step down"""
        self.move("down")
    
    def rotate(self) -> bool:
        """Rotate the current piece. Returns True if successful."""
        self.clear_piece()
        self.piece.rotate()
        colliding = self.check_collision()
        if colliding != 0:
            self.piece.rotate("counterclockwise")
        self.set_piece()
        self.new_piece = self.touching_ground()
        return colliding == 0

    def move(self, direction) -> bool:
        """Move the current piece in the given direction. Returns True if the move was successful."""
        opposites = {"left": "right", "right": "left", "down": "up", "up": "down"}
        self.clear_piece()
        self.piece.translate(direction)
        colliding = self.check_collision()
        if colliding != 0:
            self.piece.translate(opposites[direction])
        self.set_piece()
        self.new_piece = self.touching_ground()
        return colliding == 0
    
    def drop(self) -> int:
        """Drops the piece as far as it goes, and returns the distance it fell."""
        distance = 0
        while not self.new_piece:
            self.move("down")
            distance += 1
        return distance

    def clear_rows(self) -> int:
        """Clears any full rows and returns the number of rows cleared."""
        rows_cleared = 0
        for i in range(self.height):
            if " " not in self.grid[i]:
                rows_cleared += 1
                self.grid = np.delete(self.grid, i, axis=0)
                self.grid = np.concatenate([np.array([[" " for _ in range(self.width)]]), self.grid], axis=0)
        return rows_cleared

    def clear_piece(self) -> None:
        """Removes piece from grid."""
        for (i, j) in self.piece.get_coords():
            self.grid[i, j] = " "
    
    def set_piece(self) -> None:
        """Adds piece to grid."""
        for (i, j) in self.piece.get_coords():
            self.grid[i, j] = "X"

    def check_collision(self) -> int:
        """
        Check if the current piece has collided with the board and/or previous pieces.
        
        Returns:
         * 0 if no collision
         * 1 if the piece is out of bounds
         * 2 if the piece has collided with a piece already on the board
        """
        for (i, j) in self.piece.get_coords():
            if i < 0 or i >= self.height or j < 0 or j >= self.width:
                return 1
            if self.grid[i, j] != " ":
                return 2
        return 0
    
    def touching_ground(self) -> bool:
        """Check if the current piece is touching the ground or resting on another piece."""
        coords = self.piece.get_coords()
        for (i, j) in coords:
            if i == self.height - 1:
                return True
            if (i+1, j) not in coords and self.grid[i + 1, j] != " ":
                return True
        return False

    def get_row_strings(self) -> str:
        """Returns a list of strings representing the rows + boundaries of the board."""
        output = ["-" * (self.width + 2)]
        for i in range(self.height):
            s = "|"
            for j in range(self.width):
                s = s + self.grid[i][j]
            output.append(s + "|")
        output.append("-" * (self.width + 2))
        return output

    def __repr__(self) -> str:
        """String representation of the board."""
        return "\n".join(self.get_row_strings())

