
from flask_sqlalchemy import SQLAlchemy
import json
from . import bcrypt 
from . import db
#db=SQLAlchemy()

class User(db.Model):
    __tablename__='user'

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash_password=db.Column(db.String(140),unique=True,nullable=False)
    game=db.relationship('Game',backref='member',uselist=False,cascade='all , delete-orphan')
    
        
    
    def __repr__(self):
        return f'<User {self.username}>'


class Game(db.Model):  #one to one relationship,one member can have one game
    __tablename__='game'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id=db.Column(db.BigInteger,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False,unique=True)
    board = db.Column(db.JSON,nullable=False,default=json.dumps([["   " for _ in range(15)] for _ in range(15)]))
#we have serialized our board which is a 2d list which is alist that has lists and strings-which rep the cells in it. Posthress supports mostly object so in order to ensure compatibility,we create a column, db.Json is to tell postgress the type of data it is storing in our database, nullable part is that I value always has to be given, the default is that the when no value is provided this board will be used and the json.dumps serializes our 2d list into a json string
    start_position_row=db.Column(db.Integer,nullable =False,default=0)
    start_position_column=db.Column(db.Integer,nullable =False,default=0)





