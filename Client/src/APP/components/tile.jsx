import React from 'react';
import './tile.css';

const Tile = ({ letter }) => {
  const handleDragStart = (e) => {
    e.dataTransfer.setData('text/plain', letter);
  };

  return (
      <div
          className="tile"
          draggable
          onDragStart={handleDragStart}
          style={{
            width: "40px",
            height: "40px",
            margin: "5px",
            border: "1px solid blue",
            display: "inline-block",
            textAlign: "center",
            lineHeight: "40px",
            fontSize: "20px",
          }}
      >
        {letter}
      </div>
  );
};

export default Tile;
