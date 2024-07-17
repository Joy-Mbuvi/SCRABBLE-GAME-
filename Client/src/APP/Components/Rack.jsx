import React from 'react';
import Tile from './Tile';
import './Rack.css';

const Rack = ({ tiles }) => {
  return (
    <div className="rack">
      {tiles.map((tile, index) => (
        <Tile key={index} letter={tile} />
      ))}
    </div>
  );
};

export default Rack;
