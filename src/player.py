import random
from collections import Counter


class Player:
    VOWELS = ['A', 'E', 'I', 'O', 'U']
    total_racks_drawn = 0  # attribute to track the number of racks drawn

    def __init__(self, name, bag, word_dictionary):
        self.name = name
        self.score = 0
        self.rack = []
        self.bag = bag
        self.word_dictionary = word_dictionary
        self.initialize_rack()

    def initialize_rack(self, num_tiles=7):
        needed_tiles = num_tiles - len(self.rack)
        if needed_tiles > 0:
            self.rack.extend(self.bag.draw_tiles(needed_tiles))
        Player.total_racks_drawn += 1
        self.ensure_vowels_and_consonants()

    def ensure_vowels_and_consonants(self):
        if Player.total_racks_drawn <= 15:
            vowels = [tile for tile in self.rack if tile.letter in self.VOWELS]
            consonants = [tile for tile in self.rack if tile.letter not in self.VOWELS]

            if len(vowels) < 2:
                self.add_vowels(2 - len(vowels))

            if len(consonants) < 2:
                self.add_consonants(2 - len(consonants))

    def add_vowels(self, count):
        for _ in range(count):
            # Remove a random non-vowel tile from the rack
            non_vowel_tiles = [tile for tile in self.rack if tile.letter not in self.VOWELS]
            if non_vowel_tiles:
                removed_tile = non_vowel_tiles.pop(random.randint(0, len(non_vowel_tiles) - 1))
                self.rack.remove(removed_tile)
                # Draw a vowel tile from the bag
                vowel_tiles = [tile for tile in self.bag.bag if tile.letter in self.VOWELS]
                if vowel_tiles:
                    new_vowel_tile = random.choice(vowel_tiles)
                    self.rack.append(new_vowel_tile)
                    self.bag.bag.remove(new_vowel_tile)

    def add_consonants(self, count):
        for _ in range(count):
            # Remove a random vowel tile from the rack
            vowel_tiles = [tile for tile in self.rack if tile.letter in self.VOWELS]
            if vowel_tiles:
                removed_tile = vowel_tiles.pop(random.randint(0, len(vowel_tiles) - 1))
                self.rack.remove(removed_tile)
                # Draw a consonant tile from the bag
                consonant_tiles = [tile for tile in self.bag.bag if tile.letter not in self.VOWELS]
                if consonant_tiles:
                    new_consonant_tile = random.choice(consonant_tiles)
                    self.rack.append(new_consonant_tile)
                    self.bag.bag.remove(new_consonant_tile)

    def remove_tiles(self, tiles):
        for tile in tiles:
            for rack_tile in self.rack:
                if tile == rack_tile.letter:
                    self.rack.remove(rack_tile)
                    break

    def display_rack(self):
        rack_counter = Counter(tile.letter for tile in self.rack)
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

    def refill_rack(self, num_tiles=7):
        needed_tiles = num_tiles - len(self.rack)
        if needed_tiles > 0:
            self.rack.extend(self.bag.draw_tiles(needed_tiles))
        self.ensure_vowels_and_consonants()