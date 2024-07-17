// BoardTile.js
import React from 'react';
import './Board.css';

const BoardTile = ({ index, onDropTile }) => {
    const handleDragOver = (e) => {
        e.preventDefault();
    };

    const handleDrop = (e) => {
        e.preventDefault();
        const letter = e.dataTransfer.getData('text/plain');
        onDropTile(letter, index);
    };

    return (
        <div
            className="board-tile"
            onDragOver={handleDragOver}
            onDrop={handleDrop}
        >
            {/* Tile content can go here if needed */}
        </div>
    );
};

export default BoardTile;
