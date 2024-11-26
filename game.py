from board import Board
import piece
import time as t

class Game:
    def __init__(self):
        self.board = Board(piece.random_piece())
        self.score = 0
        self.next_piece = None
        self.reserve_piece = None

    def step(self):
        self.board.step()
        if self.board.new_piece:
            self.board.add_piece(self.next_piece)
            self.set_next_piece()

    def set_next_piece(self):
        self.next_piece = piece.random_piece()

# actually run the game
if __name__ == "__main__":
    g = Game()
    g.set_next_piece()
    while True:
        g.step()
        print(g.board.grid)
        t.sleep(0.1)
