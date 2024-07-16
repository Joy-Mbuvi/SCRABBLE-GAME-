import random
class Tile:
    def __init__(self, letter, tile_points):
        self.letter = letter
        self.points = tile_points

        

tile_frequencies = {
    'A': 9, 'B': 2, 'C': 2, 'D': 4, 'E': 12, 'F': 2, 'G': 3, 'H': 2, 'I': 9, 'J': 1, 'K': 1, 'L': 4,
    'M': 2, 'N': 6, 'O': 8, 'P': 2, 'Q': 1, 'R': 6, 'S': 4, 'T': 6, 'U': 4, 'V': 2, 'W': 2, 'X': 1,
    'Y': 2, 'Z': 1
}

class TileBag:
    def __init__(self, tile_points):
        self.tile_points = tile_points
        self.bag = []
        self.initialize_bag()

    def initialize_bag(self):
        for letter, frequency in tile_frequencies.items():
            for _ in range(frequency):
                self.bag.append(Tile(letter, self.tile_points))

    def draw_tiles(self, num_of_tiles):
        drawn_tiles = random.sample(self.bag, num_of_tiles)
        for tile in drawn_tiles:
            self.bag.remove(tile)
        return drawn_tiles

    def return_tiles(self, returned_tiles):
        self.bag.extend(returned_tiles)
