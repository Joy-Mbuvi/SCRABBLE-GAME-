// Tile.js
import React from 'react';
import { useDrag } from 'react-dnd';
import './Tile.css';

const Tile = ({ letter }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'TILE',
    item: { letter },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));

  return (
      <div
          ref={drag}
          className="tile"
          style={{ opacity: isDragging ? 0.5 : 1 }}
      >
        {letter}
      </div>
  );
};

export default Tile;
