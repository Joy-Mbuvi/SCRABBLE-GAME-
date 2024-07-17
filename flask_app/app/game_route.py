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

@game_blueprint.route("/game/board",methods=["GET"])
@jwt_required() 
def get_board():
    current_user= get_jwt_identity() 
    game= Game.query.filter_by(user_id=current_user['id']).first()
    if not game:
        return jsonify({'message': "oops Game not found"}),400
    board=json.loads(game.board) 
    return jsonify ({'message':f"HI {current_user['username']} we present your board",'board':board})

@game_blueprint.route("/game/make-move",methods=["PUT"])
@jwt_required()
def move():
    current_user= get_jwt_identity()
    game= Game.query.filter_by(user_id=current_user['id']).first()
    if not game:
        return jsonify({'message': "oops Game not found"}),400

    body=request.get_json()
    direction_right = body.get('right')
    direction_down= body.get('down')
    x=to_int(body.get('x'))
    y= to_int(body.get('y'))
    word=body.get('word')

    if x is None or y is None or not word:
        return jsonify({'message': "Invalid Input"}),400
    

    board=json.loads(game.board) #tupate state ya board

    moves_possible=(board,word,x,y,direction_right,direction_down)
    
    
    found_move= None

    for move in moves_possible:
        if move ['x']==x and move['y']==y and move['direction_right'] == direction_right:
            found_move=True
            break
        elif move ['x']==x and move['y']==y and move['direction_down'] == direction_down:
              found_move=True
              break
    if not found_move:
        return jsonify({'message': "chose another move"})
    
    
    board_instance.update_board(board,word,x,y,direction_down,direction_right)

 # hapa ndio ensure kuturn switching uses the correct instances of Player and ComputerPlayer
    if game.current_turn ==  'player' :
        game.current_turn= 'computer'
        computer_move=generate_move(board)
        board_instance.update_board(board, computer_move['word'], computer_move['x'], computer_move['y'], computer_move['direction_right'], computer_move['direction_down'])

     # Save the updated game state
    game.board = json.dumps(board)
    db.session.commit()

    return jsonify({'message': f"Hi {current_user['username']} we present your board", 'board': board})

@game_blueprint.route("/game/possible-move", methods=["GET"])
@jwt_required()
def possible_moves():
    current_user= get_jwt_identity() 
    game= Game.query.filter_by(user_id=current_user['id']).first()
    if not game:
        return jsonify({'message': "oops Game not found"}),400
    board=Board()
    board.board=json.loads(game.board)

    player_tiles=session.get('player_tiles')
    if not player_tiles:
        return jsonify({'message': "Player tiles not found in session"})
    
    possible_moves= calculate_possible_moves(board,player_tiles)

    return jsonify({'possible_moves':possible_moves})

def calculate_possible_moves(board, player_tiles):
    possible_moves = []
    potential_words = generate_possible_words(player_tiles) 

    for row in range(15):
        for col in range(15):
            for word in potential_words:
                if board.is_cell_available(word, 'right', col, row) and board.check_intersection(word, 'right', col, row):
                    possible_moves.append({'word': word, 'direction': 'right', 'col': col, 'row': row})
                if board.is_cell_available(word, 'down', col, row) and board.check_intersection(word, 'down', col, row):
                    possible_moves.append({'word': word, 'direction': 'down', 'col': col, 'row': row})

    return possible_moves

words=set(WORD_DICTIONARY)
def generate_possible_words(player_tiles):
    possible_words = set()
    
    
    for length in range(1, len(player_tiles) + 1):  
        for combination in itertools.combinations(player_tiles, length):  
            word = ''.join(combination)  
            if word in words:  
                possible_words.add(word)  

    return list(possible_words)  

@game_blueprint.route("/game/new-game",methods=["GET"])
@jwt_required()
def start_new_game():
    current_user=get_jwt_identity()
    game=Game.query.filter_by(member_id=current_user['id']).first()
    if game:
        return jsonify({'message':'game exist'})
    else:
        game= Game(user_id=current_user['id'])
        db.session.add(game)

    board=get_board()
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
        
    
    return jsonify({
        'message': "New game started",
        'board': board,
        'player_tiles': player_tiles
    })

def create_board():
    return [["   " for _ in range(15)] for _ in range(15)]