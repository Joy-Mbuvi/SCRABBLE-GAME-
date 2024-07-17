import React from 'react';
import { useDrag, useDrop } from 'react-dnd';
import './Tile.css';

const Tile = ({ letter, position, onDrop }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'tile',
    item: { letter, position },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }));

  const [, drop] = useDrop(() => ({
    accept: 'tile',
    drop: (item, monitor) => {
      const delta = monitor.getDifferenceFromInitialOffset();
      const direction = delta.x > delta.y ? 'right' : 'down';  // Simplistic direction detection
      onDrop(item, { ...position, direction });
    },
  }));

  return (
    <div
      ref={(node) => drag(drop(node))}
      className="tile"
      style={{ opacity: isDragging ? 0.5 : 1 }}
    >
      {letter}
    </div>
  );
};

export default Tile;
