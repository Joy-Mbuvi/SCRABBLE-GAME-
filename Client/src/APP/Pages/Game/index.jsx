import React from 'react';
import Board from '../../Components/Board';
import Rack from '../../Components/Rack';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import './Game.css';

const Game = () => {
  const rackTiles = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="game-container">
        <h1>Scrabble Game</h1>
        <Board />
        <Rack tiles={rackTiles} />
      </div>
    </DndProvider>
  );
};

export default Game;
