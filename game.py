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
        self.lines_cleared = 0  # specifically, lines cleared at this particular level

    def step(self) -> None:
        """One time step of the game. Also where score/level checks are."""
        # add a new piece to the board?
        if self.board.new_piece:
            # update score
            lines_cleared = self.board.clear_rows()
            self.lines_cleared += lines_cleared
            self.add_score(ROW_SCORES[lines_cleared] * (self.level+1))
            # initialize the next piece
            self.board.add_piece(piece.piece_from_letter(self.next_piece.letter))
            self.set_next_piece()
            # do a level-up check: level up by clearing (10 * level) lines
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

        self.board.step()

    def set_next_piece(self) -> None:
        """Set a random next piece to be added to the board."""
        self.next_piece = piece.random_piece()

    def refresh_board(self) -> None:
        """Refresh the terminal display of the game state."""
        self.stdscr.erase()
        s = str(self)
        self.stdscr.addstr(str(self))
        self.stdscr.refresh()
    
    def add_score(self, score) -> None:
        """Update the score."""
        self.score += score

    def swap_pieces(self) -> None:
        """Put the current piece in reserve, and replace with reserve/new (if there is no reserve) piece."""
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
    
    def __repr__(self) -> str:
        """Returns string representation of the game state."""
        title_row = "TETRIS"
        score_row = "Score: " + str(self.score)
        level_row = "Level: " + str(self.level)
        next_piece_rows = self.next_piece.get_row_strings()
        next_piece_rows = ["Next piece: " + next_piece_rows[0]] + next_piece_rows[1:]
        if self.reserve_piece:
            reserve_rows = self.reserve_piece.get_row_strings()
            reserve_rows = ["Reserve piece: " + reserve_rows[0]] + reserve_rows[1:]
        else:
            reserve_rows = ["Reserve piece: None"]
        spacer = "  "

        # TODO: this works but is messy
        output = ""
        next_piece_ndx = 0
        reserve_piece_ndx = 0
        for i, row in enumerate(self.board.get_row_strings()):
            if i == 6:
                output += row + spacer + title_row
            elif i == 7:
                output += row
            elif i == 8:
                output += row + spacer + level_row
            elif i == 9:
                output += row + spacer + score_row
            elif i == 10:
                output += row + spacer + next_piece_rows[0]
                next_piece_ndx = i
            elif next_piece_ndx and (0 < (i - next_piece_ndx) < len(next_piece_rows)):
                output += row + (" " * (12 + len(spacer))) + next_piece_rows[i - next_piece_ndx]
            elif next_piece_ndx and reserve_piece_ndx == 0:
                output += row + spacer + reserve_rows[0]
                reserve_piece_ndx = i
            elif next_piece_ndx and (0 < (i - reserve_piece_ndx) < len(reserve_rows)):
                output += row + (" " * (15 + len(spacer))) + reserve_rows[i - reserve_piece_ndx]
            else:
                output += row
            output += "\n"
        return output[:-1]

# actually run the game
if __name__ == "__main__":
    g = Game()
    step_time = t.time()
    while True:
        # key controls
        user_input = g.stdscr.getch()
        if user_input == curses.KEY_RIGHT or user_input == 100:  # 'd'
            g.board.move("right")
            g.refresh_board()
        elif user_input == curses.KEY_LEFT or user_input == 97:  # 'a'
            g.board.move("left")
            g.refresh_board()
        elif user_input == curses.KEY_UP or user_input == 119:  # 'w'
            g.board.rotate()
            g.refresh_board()
        elif user_input == curses.KEY_DOWN or user_input == 115:  # 's'
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