import random
from string import ascii_uppercase
from collections import Counter

WORD_DICTIONARY = {"APPLE", "BANANA"}

LETTER_POINTS = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1,
    'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
    'Y': 4, 'Z': 10
}

class Tile:
    def __init__(self, letter, LETTER_POINTS={}):
        self.letter = letter
        self.LETTER_POINTS = LETTER_POINTS.get(letter, 0)

tiles = [Tile(letter, LETTER_POINTS) for letter in LETTER_POINTS.keys()]

class Tile_bag:
    def __init__(self, bag):
        self.bag = bag.copy()

    def refill(self):
        self.bag = tiles.copy()

    def draw_tiles(self, num_of_tiles):
        drawn_tiles = random.sample(self.bag, num_of_tiles)
        for tile in drawn_tiles:
            self.bag.remove(tile)
        return drawn_tiles

    def return_tiles(self, returned_tiles):
        self.bag.extend(returned_tiles)

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.rack = []
        self.initialize_rack()

    def initialize_rack(self, num_tiles=7):
        while len(self.rack) < num_tiles:
            word = random.choice(list(WORD_DICTIONARY))
            scrambled_word = list(word)
            random.shuffle(scrambled_word)
            self.rack.extend(scrambled_word)
            self.rack = self.rack[:num_tiles]  # Ensure rack has exactly num_tiles

    def refill_rack(self):
        self.initialize_rack()

    def remove_tiles(self, tiles):
        for tile in tiles:
            if tile in self.rack:
                self.rack.remove(tile)

    def display_rack(self):
        rack_counter = Counter(self.rack)
        rack_display = ", ".join(f"{letter}({count})" for letter, count in rack_counter.items())
        return f"{self.name}'s Rack: {rack_display}"

    def update_score(self, word_score):
        self.score += word_score

    def get_score(self):
        return self.score

    def shuffle_rack(self):
        random.shuffle(self.rack)

    def set_rack(self, rack):
        self.rack = rack

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

class ComputerPlayer(Player):
    def generate_move(self, board):
        valid_word = False
        while not valid_word:
            word_to_play = random.choice(list(WORD_DICTIONARY))
            word_length = len(word_to_play)
            if random.random() < 0.5:
                direction = "right"
                max_col = 15 - word_length
                col = random.randint(0, max_col)
                row = random.randint(0, 14)
            else:
                direction = "down"
                col = random.randint(0, 14)
                max_row = 15 - word_length
                row = random.randint(0, max_row)

            if direction == "right":
                if all(board.board[row][col + i] == "   " for i in range(word_length)):
                    valid_word = True
            elif direction == "down":
                if all(board.board[row + i][col] == "   " for i in range(word_length)):
                    valid_word = True

            if word_to_play in Word.played_words:
                valid_word = False

        return word_to_play, [row, col], direction

def turn(player, board, bag):
    global round_number, skipped_turns

    if len(Word.played_words) == len(WORD_DICTIONARY):
        end_game()
        return

    if skipped_turns < 6 or (len(player.rack) == 0 and len(bag.bag) == 0):
        print("\nRound " + str(round_number) + ": " + player.name + "'s turn \n")
        board.display_board()
        print(player.display_rack())

        if isinstance(player, ComputerPlayer):
            word_to_play, location, direction = player.generate_move(board)
            word = Word(word_to_play, location, player, direction, board.board)
        else:
            valid_word = False
            while not valid_word:
                word_to_play = input("Word to play (or type 'SHUFFLE' to shuffle your rack): ").upper()
                if word_to_play == "SHUFFLE":
                    player.shuffle_rack()
                    print("Rack shuffled. New rack:")
                    print(player.display_rack())
                    continue
                if word_to_play in WORD_DICTIONARY and word_to_play not in Word.played_words:
                    valid_word = True
                    row = int(input("Row number: "))
                    col = int(input("Column number: "))
                     
                    direction = input("Direction of word (right or down): ").lower()

                    word = Word(word_to_play, (col, row), player, direction, board.board)
                else:
                    print("Invalid word. Try again.")

        if word_to_play == "":
            print("Turn skipped.")
            skipped_turns += 1
        else:
            if word.check_word():
                word.calculate_word_score()
                word.place_on_board() 
                player.remove_tiles(word_to_play)
                player.refill_rack()
                # Display the word played and its score
                print(f"\n{player.name} played '{word.get_word()}' for {word.score} points.")
            else:
                print("Invalid word placement.")
            skipped_turns = 0

        print(f"\n{player.name}'s score is: {player.get_score()}")

        if players.index(player) != (len(players) - 1):
            next_player = players[players.index(player) + 1]
        else:
            next_player = players[0]
            round_number += 1

        turn(next_player, board, bag)
    else:
        end_game()


def start_game():
    global round_number, players, skipped_turns
    board = Board()
    bag = Tile_bag(tiles)
    
    num_of_players = int(input("\nIf 1 + 1 = 2, what is 2 - 1 = "))
    while num_of_players != 1:
        num_of_players = int(input("Sorry, try again. You don't need Magic. What is 2 - 1 = "))
    print("Correct! Now we can proceed.")

    print("\nWelcome to Scrabble! Please enter your name.")
    players = []
    for i in range(num_of_players):
        player_name = input("Please enter player your name: ")
        players.append(Player(player_name))
    
    players.append(ComputerPlayer("Computer"))
    
    round_number = 1
    skipped_turns = 0
    current_player = players[0]
    turn(current_player, board, bag)

def end_game():
    global players
    highest_score = 0
    winning_player = ""
    for player in players:
        if player.get_score() > highest_score:
            highest_score = player.get_score()
            winning_player = player.name
    print("The game is over! " + winning_player + ", won!")
    
    if input("\nWould you like to play again? (y/n)").upper() == "Y":
        print("Restart the Game")

if __name__ == "__main__":
    start_game()