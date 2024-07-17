// Tile.js
import React from 'react';
import './Tile.css';

const Tile = ({ letter }) => {
  const handleDragStart = (e) => {
    e.dataTransfer.setData('text/plain', letter);
  };

  return (
      <div
          className="tile"
          draggable
          onDragStart={handleDragStart}
      >
        {letter}
      </div>
  );
};

export default Tile;
