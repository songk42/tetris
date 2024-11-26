import curses
import piece
import sys
import time as t

from board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.next_piece = piece.random_piece()
        self.reserve_piece = None
        self.step_interval = 1  # seconds between each step
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(1)
        self.stdscr.keypad(1)
        # curses.cbreak()
        # curses.nonl()
        # curses.curs_set(0)
        # curses.noecho()

    def step(self):
        self.board.step()
        # somewhere along here, I think some pieces sink down one more level than they should
        # maybe it's because of those down-arrow inputs
        if self.board.new_piece:
            rows_cleared = self.board.clear_rows()
            self.board.add_piece(piece.piece_from_letter(self.next_piece.letter))
            self.set_next_piece()
        if self.board.game_over:
            print("Game over!")
            print("Score:", self.score)
            exit()

    def set_next_piece(self):
        self.next_piece = piece.random_piece()

    def refresh_board(self):
        self.stdscr.erase()
        self.stdscr.addstr(str(self.board))
        self.stdscr.refresh()

# actually run the game
if __name__ == "__main__":
    g = Game()
    step_time = t.time()
    while True:
        # key controls
        user_input = g.stdscr.getch()
        if user_input == curses.KEY_RIGHT:
            g.board.move("right")
        elif user_input == curses.KEY_LEFT:
            g.board.move("left")
        elif user_input == curses.KEY_UP:
            g.board.rotate()
        elif user_input == curses.KEY_DOWN:
            g.board.move("down")
        elif user_input == 32:  # space bar
            g.board.drop()
        elif user_input == 113:  # 'q'
            curses.endwin()
            sys.exit(0)
        # move piece one step down
        if t.time() - step_time > g.step_interval:
            step_time = t.time()
            g.step()
        g.refresh_board()