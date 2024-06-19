class ComputerPlayer(Player):
    def generate_move(self, board):
        valid_word = False
        while not valid_word:
            word_to_play = random.choice(list(WORD_DICTIONARY))
            word_length = len(word_to_play)

            if len(Word.played_words) == 0:  # First move must start at the center
                direction = random.choice(["right", "down"])
                row, col = 7, 7
                if direction == "right" and col + word_length <= 15:
                    valid_word = True
                elif direction == "down" and row + word_length <= 15:
                    valid_word = True
            else:
                for row in range(15):
                    for col in range(15):
                        if board.board[row][col] != "   ":
                            for i in range(word_length):
                                if col + i < 15 and all(board.board[row][col + j] in ["   ", f" {word_to_play[j]} "] for j in range(word_length)):
                                    direction = "right"
                                    if any(board.board[row][col + j] != "   " for j in range(word_length)):
                                        valid_word = True
                                        break
                                if row + i < 15 and all(board.board[row + j][col] in ["   ", f" {word_to_play[j]} "] for j in range(word_length)):
                                    direction = "down"
                                    if any(board.board[row + j][col] != "   " for j in range(word_length)):
                                        valid_word = True
                                        break
                        if valid_word:
                            break
                    if valid_word:
                        break

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
                    if len(Word.played_words) == 0:
                        row, col = 7, 7
                        direction = input("Direction of word (right or down): ").lower()
                    else:
                        row = int(input("Row number: "))
                        col = int(input("Column number: "))
                        direction = input("Direction of word (right or down): ").lower()
                        if direction not in ["right", "down"]:
                            print("Invalid direction. Try again.")
                            valid_word = False
                            continue

                        if not board.is_cell_available(word_to_play, direction, col, row):
                            print("Word cannot be placed there. Try again.")
                            valid_word = False
                            continue

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
        start_game()

if __name__ == "__main__":
    start_game()