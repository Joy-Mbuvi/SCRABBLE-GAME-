from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from .models import Game
from .src.board_and_management import Board
from .src.scrabble import WORD_DICTIONARY
from .src.tile_and_bag import TileBag
from .src.computer_player import *
import itertools
import json
from .util import to_int


game_blueprint=Blueprint('game',__name__)

@game_blueprint.route("/game/board", methods=["GET"])
@jwt_required()
def get_board():
    current_user = get_jwt_identity()
    game = Game.query.filter_by(user_id=current_user['id']).first()

    if not game:
        new_board = [[" " for _ in range(15)] for _ in range(15)]
        new_board[7][7] = "X"
        game = Game(
            user_id=current_user['id'],
            board=json.dumps(new_board)
        )
        db.session.add(game)
        db.session.commit()

    board = json.loads(game.board)
    return jsonify({'message': f"HI {current_user['username']} we present your board", 'board': board})


@game_blueprint.route("/game/make-move", methods=["PUT"])
@jwt_required()
def move():
    current_user = get_jwt_identity()
    game = Game.query.filter_by(user_id=current_user['id']).first()
    if not game:
        return jsonify({'message': "Oops, game not found"}), 400

    body = request.get_json()
    direction = body.get('direction')
    x = to_int(body.get('x'))
    y = to_int(body.get('y'))
    word = body.get('word')

    if x is None or y is None or not word or not direction:
        return jsonify({'message': "Invalid input"}), 400

    board = json.loads(game.board)
    board_instance = Board()
    board_instance.board = board

    
    if board_instance.is_cell_available(word, direction, x, y) or board_instance.check_intersection(word, direction, x, y):
            updated_board = board_instance.update_board(word, direction, x, y)
            if updated_board:
                game.board = json.dumps(updated_board)
                db.session.commit()
                return jsonify({'message': f"Hi {current_user['username']}, here is your updated board", 'board': updated_board})
            else:
                return jsonify({'message': "Failed to update the board"}), 400
    else:
            return jsonify({'message': "Invalid move: Cell not available or word does not intersect correctly"}), 400


@game_blueprint.route("/game/rack", methods=["GET"])
@jwt_required()
def get_rack():
    current_user = get_jwt_identity()
    game = Game.query.filter_by(user_id=current_user['id']).first()
    if not game:
        return jsonify({'message': "Oops, game not found"}), 400

    player_tiles = session.get('player_tiles')
    if not player_tiles:
        # Draw new tiles for the user
        tile_points = {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1,
            'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
            'Y': 4, 'Z': 10
        }
        tile_bag = TileBag(tile_points)
        player_tiles = tile_bag.draw_tiles(7)
        
        # Convert player tiles to a list of letters for storing in the session
        player_tiles_letters = [tile.letter for tile in player_tiles]
        session['player_tiles'] = player_tiles_letters
        player_tiles = player_tiles_letters


    return jsonify({'player_tiles': player_tiles})


# @game_blueprint.route("/game/possible-move", methods=["GET"])
# @jwt_required()
# def possible_moves():
#     current_user= get_jwt_identity() 
#     game= Game.query.filter_by(user_id=current_user['id']).first()
#     if not game:
#         return jsonify({'message': "oops Game not found"}),400
#     board=Board()
#     board.board=json.loads(game.board)

#     player_tiles=session.get('player_tiles')
#     if not player_tiles:
#         return jsonify({'message': "Player tiles not found in session"})
    
#     possible_moves= calculate_possible_moves(board,player_tiles)

#     return jsonify({'possible_moves':possible_moves})

# def calculate_possible_moves(board, player_tiles):
#     possible_moves = []
#     potential_words = generate_possible_words(player_tiles) 

#     for row in range(15):
#         for col in range(15):
#             for word in potential_words:
#                 if board.is_cell_available(word, 'right', col, row) and board.check_intersection(word, 'right', col, row):
#                     possible_moves.append({'word': word, 'direction': 'right', 'col': col, 'row': row})
#                 if board.is_cell_available(word, 'down', col, row) and board.check_intersection(word, 'down', col, row):
#                     possible_moves.append({'word': word, 'direction': 'down', 'col': col, 'row': row})

#     return possible_moves

# words=set(WORD_DICTIONARY)
# def generate_possible_words(player_tiles):
#     possible_words = set()
    
    
#     for length in range(1, len(player_tiles) + 1):  
#         for combination in itertools.combinations(player_tiles, length):  
#             word = ''.join(combination)  
#             if word in words:  
#                 possible_words.add(word)  

#     return list(possible_words)  

@game_blueprint.route("/game/new-game",methods=["GET"])
@jwt_required()
def start_new_game():
    current_user=get_jwt_identity()
    game=Game.query.filter_by(user_id=current_user['id']).first()
    if game:
        return jsonify({'message':'game exist'})
    else:
        game= Game(user_id=current_user['id'])
        db.session.add(game)

    board=create_board()
    game.board=json.dumps(board)

    tile_points = {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1,
            'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
            'Y': 4, 'Z': 10
        }
    tile_bag = TileBag(tile_points)
        
        
    player_tiles = tile_bag.draw_tiles(7)
        
        
    player_tiles_letters = [tile.letter for tile in player_tiles]
    session['player_tiles']=player_tiles_letters


    db.session.commit()

    print(board)
    print(player_tiles)

    print(isinstance(player_tiles[0], TileBag))
    
    return jsonify({
        'message': "New game started",
        'board': board,
        'player_tiles': player_tiles_letters
    })

def create_board():
    return [["   " for _ in range(15)] for _ in range(15)]