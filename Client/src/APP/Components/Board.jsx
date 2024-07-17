// Board.js
import React, { useState } from 'react';
import BoardTile from './BoardTile';
import './Board.css';

const Board = () => {
  const boardSize = 15;
  const [boardTiles, setBoardTiles] = useState(Array(boardSize * boardSize).fill(null));

  const handleDropTile = (letter, index) => {
    const newBoardTiles = [...boardTiles];
    newBoardTiles[index] = letter;
    setBoardTiles(newBoardTiles);
  };

  return (
      <div className="board">
        {boardTiles.map((tile, index) => (
            <BoardTile key={index} index={index} onDropTile={handleDropTile} />
        ))}
      </div>
  );
};

export default Board;
