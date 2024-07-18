import React from 'react';
import"./tile.css"
function Tile(props) {
  const { letter } = props;

  return (
    <div
      className="tile"
      draggable
      onDragStart={(e) => e.dataTransfer.setData('text/plain', letter)}
    >
      {letter}
    </div>
  );
}

export default Tile;
