from collections import Counter
import random
from src.player import Player
from src.word import Word

class ComputerPlayer(Player):

    def generate_move(self, board, word_dictionary):
        word_to_play = ""
        col = 0
        row = 0
        direction = ""
        valid_word = False

        # Read words from dictionary, shuffle and filter
        play_words = list(word_dictionary)
        random.shuffle(play_words)
        rack_letters = [tile.letter for tile in self.rack]
        valid_words = [word for word in play_words if self.can_form_word(word, rack_letters)]

        # Check if each valid word can be placed on the board
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

    def can_form_word(self, word, rack):
        word_counter = Counter(word)
        rack_counter = Counter(rack)
        for letter in word_counter:
            if word_counter[letter] > rack_counter[letter]:
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
