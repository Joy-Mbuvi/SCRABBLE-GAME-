class Board:
    def __init__(self):
        self.board = [["   " for _ in range(15)] for _ in range(15)]
        self.board[7][7] = " X "
    
    def get_board(self): 
        board_str = "   |  " + "  |  ".join(str(item) for item in range(10)) + "  | " + "  | ".join(str(item) for item in range(10, 15)) + " |"
        board_str += ("\n   __________________________________________________________________________________________"
                      "\n")

        formatted_rows = []
        for i, row in enumerate(self.board):
            row_string = " | ".join(str(item) for item in row)
            if i < 10:
                formatted_rows.append(f"{i}  | {row_string} |")
            else:
                formatted_rows.append(f"{i} | {row_string} |")

        row_separator = ("\n   |_________________________________________________________________________________________"
                         "|\n")
        board_str += row_separator.join(formatted_rows)
        board_str += "\n   ___________________________________________________________________________________________"
        return board_str

    def update_board(self, word, orientation, x, y):
        if orientation == "Horizontal":
            for i, character in enumerate(word):
                self.board[y][x + i] = f" {character} "
        elif orientation == "Vertical":
            for i, character in enumerate(word):
                self.board[y + i][x] = f" {character} "

    def display_board(self):
        print(self.get_board())

    def is_cell_available(self, word, orientation, x, y):
        if orientation == "Horizontal":
            return all(self.board[y][x + i] == "   " or self.board[y][x + i] == f" {word[i]} " for i in range(len(word)))
        elif orientation == "Vertical":
            return all(self.board[y + i][x] == "   " or self.board[y + i][x] == f" {word[i]} " for i in range(len(word)))
        return False

    def check_intersection(self, word, direction, col, row):
        word_length = len(word)
        if direction == "Horizontal":
            for i in range(word_length):
                if self.board[row][col + i] != "   ":
                    return True
        elif direction == "Vertical":
            for i in range(word_length):
                if self.board[row + i][col] != "   ":
                    return True
        return False
