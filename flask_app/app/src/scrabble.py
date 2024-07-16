from src.board_and_management import Board
from src.computer_player import ComputerPlayer
from src.player import Player
from src.word import Word
from src.tile_and_bag import TileBag

# Define the letter points dictionary
LETTER_POINTS = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1,
    'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
    'Y': 4, 'Z': 10, ' ': 0
}

with open('dict.txt', 'r') as file:
    words = [word.strip().upper() for word in file.readlines()]

WORD_DICTIONARY = set(words)

def turn(player, board, bag):

    global round_number

    if len(Word.played_words) == len(WORD_DICTIONARY):
        end_game()
        return

    print("\nRound " + str(round_number) + ": " + player.name + "'s turn \n")
    board.display_board()
    print(player.display_rack())

    if isinstance(player, ComputerPlayer):
        word_to_play, location, direction = player.generate_move(board, WORD_DICTIONARY)
        word = Word(word_to_play, location, player, direction, board.board, WORD_DICTIONARY, LETTER_POINTS)
    else:
        valid_word = False
        while not valid_word:
            word_to_play = input("Word to play (or type 'SHUFFLE' to shuffle your rack): ").upper()
            if word_to_play == "SHUFFLE":
                player.shuffle_rack()
                print("Rack shuffled. New rack:")
                print(player.display_rack())
                continue
            if word_to_play.strip() == "":
                break
            if word_to_play in WORD_DICTIONARY and word_to_play not in Word.played_words:
                if len(Word.played_words) == 0:
                    row, col = 7, 7
                    direction = input("Direction of word (right or down): ").lower()
                    valid_word = True     
                else:
                    row = int(input("Row number: "))
                    col = int(input("Column number: "))
                    direction = input("Direction of word (right or down): ").lower()
                    if direction not in ["right", "down"]:
                        print("Invalid direction. Try again.")
                        continue

                    if (board.is_cell_available(word_to_play, direction, col, row)
                            and board.check_intersection(word_to_play, direction, col, row)
                            and word_to_play in WORD_DICTIONARY):
                        valid_word = True
                    else:
                        print("Word cannot be placed there or does not intersect with an existing word. Try again.")

                word = Word(word_to_play, (col, row), player, direction, board.board, WORD_DICTIONARY, LETTER_POINTS)
            else:
                print("Invalid word. Try again.")

    if word_to_play == "":
        print("Turn skipped.")
    else:
        
        word.calculate_word_score()
        word.place_on_board()
        player.remove_tiles(word_to_play)
        player.refill_rack()
        print(f"\n{player.name} played '{word.get_word()}' for {word.get_score()} points.")
    
    

    print(f"\n{player.name}'s score is: {player.get_score()}")

    if players.index(player) != (len(players) - 1):
        next_player = players[players.index(player) + 1]
    else:
        next_player = players[0]
        round_number += 1

    turn(next_player, board, bag)

def start_game():
    global round_number, players
    board = Board()
    bag = TileBag(tile_points= LETTER_POINTS)

    num_of_players = 1

    print("\nWelcome to Our Scrabble World!")
    players = []
    for i in range(num_of_players):
        player_name = input("Please enter your name: ")
        players.append(Player(player_name, bag, WORD_DICTIONARY))

    players.append(ComputerPlayer("Computer", bag, WORD_DICTIONARY))

    round_number = 1
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
    print("The game is over! " + winning_player + " won!")

    if input("\nWould you like to play again? (y/n)").upper() == "Y":
        print("Restart the Game")
        start_game()

if __name__ == "__main__":
    start_game()