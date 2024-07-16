class Word:
    played_words = set()

    def __init__(self, word, location, player, direction, board, word_dictionary, tile_points):
        self.word = word
        self.location = location #starting point
        self.player = player
        self.direction = direction
        self.board = board
        self.score = 0
        self.word_dictionary = word_dictionary
        self.tile_points = tile_points

    def check_word(self):
        if self.word.upper() in self.word_dictionary and self.word.upper() not in Word.played_words:
            return True
        else:
            return False

    def calculate_word_score(self):
        self.score = sum(self.tile_points[letter] for letter in self.word)
        self.player.update_score(self.score)
        Word.played_words.add(self.word.upper())

    def place_on_board(self):
        x, y = self.location
        if self.direction == "right":
            for i, char in enumerate(self.word):
                if (x+i) < 15:
                 self.board[y][x + i] = f" {char} "
        elif self.direction == "down":
            for i, char in enumerate(self.word):
                if (y+i) < 15:
                 self.board[y + i][x] = f" {char} "

    def get_word(self):
        return self.word 

    def get_score(self):
        return self.score
