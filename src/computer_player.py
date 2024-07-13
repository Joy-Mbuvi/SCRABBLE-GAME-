from src.player import Player
import random
from src.word import Word

class ComputerPlayer(Player):

    def generate_move(self, board, word_dictionary):
        word_to_play = ""
        col = 0
        row = 0
        direction = ""
        valid_word = False

        # hii inachukuwa words za dictionary inaassign to play words then inashuffle ndio a random word ichaguliwe
        play_words = list(word_dictionary)
        random.shuffle(play_words)

        # Filter words that can be formed from the rack
        rack_letters = [tile.letter for tile in self.rack]
        valid_words = [word for word in play_words if self.word_from_rack(word, rack_letters)]

        # Iterate through the filtered list in the valid words and check if it can be placed on the board
        for word in valid_words:
            for row in range(15):
                for col in range(15):
                    if board.board[row][col] != "":
                        if self.can_place_word(board, word, row, col, "right"):
                            word_to_play = word
                            direction = "right"
                            valid_word = True
                            break
                        if self.can_place_word(board, word, row, col, "down"):
                            word_to_play = word
                            direction = "down"
                            valid_word = True
                            break
                if valid_word:
                    break
            if valid_word:
                break

        return word_to_play, [col, row], direction

    def word_from_rack(self, word, rack): #will remove the letters(tiles) that have been chosen from the rack 
        rack_copy = rack.copy()
        for letter in word:
            if letter in rack_copy:
                rack_copy.remove(letter)
            else:
                return False
        return True

    def can_place_word(self, board, word, row, col, direction):
        word_length = len(word)

        if direction == "right":
            if col + word_length > 15:  # Ensure word fits horizontally
                return False
            for j in range(word_length):
                if not (board.board[row][col + j] == "   " or board.board[row][col + j] == f" {word[j]} "):
                    return False
            if not any(board.board[row][col + j] != "   " for j in range(word_length)):
                return False
        elif direction == "down":
            if row + word_length > 15:  # Ensure word fits vertically
                return False
            for j in range(word_length):
                if not (board.board[row + j][col] == "   " or board.board[row + j][col] == f" {word[j]} "):
                    return False
            if not any(board.board[row + j][col] != "   " for j in range(word_length)):
                return False

        return True
