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
        if orientation == "Right":
            for i, character in enumerate(word):
                self.board[y][x + i] = f" {character} "
        elif orientation == "Down":
            for i, character in enumerate(word):
                self.board[y + i][x] = f" {character} "

    def display_board(self):
        print(self.get_board())

    # def is_cell_available(self, word, orientation, x, y):
    #     if orientation == "Right":
    #         return all(self.board[y][x + i] == "   " or self.board[y][x + i] == f" {word[i]} " for i in range(len(word)))
    #     elif orientation == "Down":
    #         return all(self.board[y + i][x] == "   " or self.board[y + i][x] == f" {word[i]} " for i in range(len(word)))
    #     return False
    def is_cell_available(self, word, direction, col, row):
        if direction == "right":
            for i, char in enumerate(word):
                if col + i >= 15 or (self.board[row][col + i] != "   " and self.board[row][col + i].strip() != char):
                    return False
        elif direction == "down":
            for i, char in enumerate(word):
                if row + i >= 15 or (self.board[row + i][col] != "   " and self.board[row + i][col].strip() != char):
                    return False
        return True
    def check_intersection(self, word, direction, col, row):
        word_length = len(word)
        intersects = False
    
        if direction == "right":
            for i in range(word_length):
                if self.board[row][col + i] != "   ":
                    intersects = True
        elif direction == "down":
            for i in range(word_length):
                if self.board[row + i][col] != "   ":
                     intersects = True

        return intersects


    # def check_intersection(self, word, direction, col, row):
    #     word_length = len(word)
    #     if direction == "Right":
    #         for i in range(word_length):
    #             if self.board[row][col + i] != "   ":
    #                 return True
    #     elif direction == "Down":
    #         for i in range(word_length):
    #             if self.board[row + i][col] != "   ":
    #                 return True
    #     return False
