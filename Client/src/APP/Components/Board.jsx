import React from 'react';
import './Board.css';

const Board = () => {
  const boardSize = 15;
  const tiles = Array.from({ length: boardSize * boardSize }, (_, index) => (
    <div key={index} className="board-tile">
      {/* Tile content can go here if needed */}
    </div>
  ));

  return <div className="board">{tiles}</div>;
};

export default Board;
