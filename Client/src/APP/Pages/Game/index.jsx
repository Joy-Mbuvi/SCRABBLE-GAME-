// Game.js
import React, { useEffect, useState } from 'react';
import Board from '../../Components/Board';
import Rack from '../../Components/Rack';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import './Game.css';
import axios from 'axios';

const Game = () => {
    const [rackTiles, setRackTiles] = useState(['A', 'B', 'C', 'D', 'E', 'F', 'G']);

    const getRackLetters = () => {
        // axios({
        //     method: 'GET',
        //     url: 'https://127.0.0.1:5000',
        // });
    };

    useEffect(() => {
        getRackLetters();
    }, []);

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
