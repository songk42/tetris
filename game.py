import curses
import piece
import sys
import time as t

from board import Board

ROW_SCORES = [0, 40, 100, 300, 1200]

class Game:
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.level = 1
        self.next_piece = piece.random_piece()
        self.reserve_piece = None
        self.step_interval = 0.8  # seconds between each step
        self.stdscr = curses.initscr()  # the thing that prints to the terminal
        self.stdscr.nodelay(1)
        self.stdscr.keypad(1)
        self.lines_cleared = 0
        # curses.cbreak()
        # curses.nonl()
        # curses.curs_set(0)
        # curses.noecho()

    def step(self):
        self.board.step()
        # time to add a new piece to the board
        if self.board.new_piece:
            # update score
            lines_cleared = self.board.clear_rows()
            self.lines_cleared += lines_cleared
            self.add_score(ROW_SCORES[lines_cleared] * (self.level+1))
            # initialize the next piece
            self.board.add_piece(piece.piece_from_letter(self.next_piece.letter))
            self.set_next_piece()
            # do a level-up check level up by clearing 10 * level lines
            if self.lines_cleared >= 10 * self.level:
                self.level += 1
                self.lines_cleared = 0
                self.step_interval = max(0.02, self.step_interval * 0.8)  # TODO idk actually
        if self.board.game_over:
            # self.stdscr.erase()
            # self.stdscr.addstr(f"Game over!\nScore: {self.score}")
            # self.refresh_board()
            print(f"Game over!\nScore: {self.score}")
            sys.exit(0)

    def set_next_piece(self):
        self.next_piece = piece.random_piece()

    def refresh_board(self):
        self.stdscr.erase()
        s = str(self)
        self.stdscr.addstr(str(self))
        self.stdscr.refresh()
    
    def add_score(self, score):
        self.score += score

    def swap_pieces(self):
        self.board.clear_piece()
        if self.reserve_piece is None:
            # if no reserve piece already exists, store the current piece and spawn the next piece
            self.reserve_piece = self.board.piece
            self.board.add_piece(piece.piece_from_letter(self.next_piece.letter))
            self.set_next_piece()
        else:
            # if a reserve piece already exists, swap the current piece with the reserve piece
            self.reserve_piece, self.board.piece = self.board.piece, self.reserve_piece
        self.board.set_piece()
    
    def __repr__(self):
        output = str(self.board) + "\n"
        output += "Score: " + str(self.score) + "\n"
        output += "Level: " + str(self.level) + "\n"
        output += "Next piece: " + self.next_piece.letter + "\n"
        output += "Reserve piece: " + (self.reserve_piece.letter if self.reserve_piece else "None") + "\n"
        return output

# actually run the game
if __name__ == "__main__":
    g = Game()
    step_time = t.time()
    while True:
        # key controls
        user_input = g.stdscr.getch()
        if user_input == curses.KEY_RIGHT:
            g.board.move("right")
            g.refresh_board()
        elif user_input == curses.KEY_LEFT:
            g.board.move("left")
            g.refresh_board()
        elif user_input == curses.KEY_UP:
            g.board.rotate()
            g.refresh_board()
        elif user_input == curses.KEY_DOWN:
            success = g.board.move("down")
            if success: g.add_score(1)  # bonus for soft dropping
            g.refresh_board()
        elif user_input == 32:  # space bar
            dist = g.board.drop()
            g.add_score(dist)
            g.refresh_board()
        elif user_input == 99:  # 'c'
            g.swap_pieces()
            g.refresh_board()
        elif user_input == 113:  # 'q'
            curses.endwin()
            sys.exit(0)
        # move piece one step down
        if t.time() - step_time > g.step_interval:
            step_time = t.time()
            g.step()
        g.refresh_board()