import random
from collections import Counter


class Player:
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
       