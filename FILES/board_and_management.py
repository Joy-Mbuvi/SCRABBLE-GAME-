from tile_and_bag import LETTER_POINTS, WORD_DICTIONARY

class Board:
    def __init__(self):
        self.board = [["   " for _ in range(15)] for _ in range(15)]
        self.add_cells()
        self.board[7][7] = " X "

    def add_cells(self):
        TRIPLE_WORD_SCORE = [(0, 0), (7, 0), (14, 0), (0, 7), (14, 7), (0, 14), (7, 14), (14, 14)]
        DOUBLE_WORD_SCORE = [(1, 1), (2, 2), (3, 3), (4, 4), (1, 13), (2, 12), (3, 11), (4, 10),
                             (13, 1), (12, 2), (11, 3), (10, 4), (13, 13), (12, 12), (11, 11), (10, 10)]
        TRIPLE_LETTER_SCORE = [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5),
                               (9, 9), (9, 13), (13, 5), (13, 9)]
        DOUBLE_LETTER_SCORE = [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2),
                               (6, 6), (6, 8), (6, 12), (7, 3), (7, 11), (8, 2), (8, 6), (8, 8),
                               (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)]

        for co in TRIPLE_WORD_SCORE:
            self.board[co[0]][co[1]] = 'TWS'
        for co in DOUBLE_WORD_SCORE:
            self.board[co[0]][co[1]] = 'DWS'
        for co in TRIPLE_LETTER_SCORE:
            self.board[co[0]][co[1]] = 'TLS'
        for co in DOUBLE_LETTER_SCORE:
            self.board[co[0]][co[1]] = 'DLS'

    def get_board(self):
        board_str = "   |  " + "  |  ".join(str(item) for item in range(10)) + "  | " + "  | ".join(str(item) for item in range(10, 15)) + " |"
        board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"

        formatted_rows = []
        for i, row in enumerate(self.board):
            row_str = " | ".join(str(item) for item in row)
            if i < 10:
                formatted_rows.append(f"{i}  | {row_str} |")
            else:
                formatted_rows.append(f"{i} | {row_str} |")

        row_separator = "\n   |_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|\n"
        board_str += row_separator.join(formatted_rows)
        board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _"
        return board_str

    def update_board(self, word, orientation, x, y):
        if orientation == "right":
            for i, char in enumerate(word):
                self.board[y][x + i] = f" {char} "
        elif orientation == "down":
            for i, char in enumerate(word):
                self.board[y + i][x] = f" {char} "

    def display_board(self):
        print(self.get_board())

    def remove_word(self, word, direction, x, y):
        """Remove a word from the board."""
        if direction == "right":
            for i in range(len(word)):
                self.board[y][x + i] = "   "
        elif direction == "down":
            for i in range(len(word)):
                self.board[y + i][x] = "   "
                
    def is_cell_available(self, word, orientation, x, y):
        if orientation == "right":
            return all(self.board[y][x + i] == "   " for i in range(len(word)))
        elif orientation == "down":
            return all(self.board[y + i][x] == "   " for i in range(len(word)))
        return False

class Word:
    played_words = set()

    def __init__(self, word, location, player, direction, board_array):
        self.word = word
        self.location = location
        self.player = player
        self.direction = direction
        self.board_array = board_array
        self.score = 0

    def check_word(self):
        if self.word.upper() in WORD_DICTIONARY and self.word.upper() not in Word.played_words:
            return True
        else:
            return False

    def calculate_word_score(self):
        self.score = sum(LETTER_POINTS[letter] for letter in self.word)
        self.player.update_score(self.score)
        Word.played_words.add(self.word.upper())

    def place_on_board(self):
        x, y = self.location
        if self.direction == "right":
            for i, char in enumerate(self.word):
                self.board_array[y][x + i] = f" {char} "
        elif self.direction == "down":
            for i, char in enumerate(self.word):
                self.board_array[y + i][x] = f" {char} "

    def remove_from_board(self):
        x, y = self.location
        if self.direction == "right":
            for i in range(len(self.word)):
                self.board_array[y][x + i] = "   "
        elif self.direction == "down":
            for i in range(len(self.word)):
                self.board_array[y + i][x] = "   "

    def get_word(self):
        return self.word

    def get_score(self):
        return self.score