from board import Board
import piece
import time as t

class Game:
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.next_piece = piece.random_piece()
        self.reserve_piece = None

    def step(self):
        self.board.step()
        if self.board.new_piece:
            self.board.add_piece(piece.piece_from_letter(self.next_piece.letter))
            self.set_next_piece()

    def set_next_piece(self):
        self.next_piece = piece.random_piece()

# actually run the game
if __name__ == "__main__":
    g = Game()
    while True:
        g.step()
        print(g.board, flush=True)
        t.sleep(0.5)
