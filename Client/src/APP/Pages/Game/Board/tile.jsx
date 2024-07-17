import React from 'react';
import './Tile.css';

const Tile = ({ letter }) => {
  return (
    <div className="tile">
      {letter}
    </div>
  );
};

export default Tile;
