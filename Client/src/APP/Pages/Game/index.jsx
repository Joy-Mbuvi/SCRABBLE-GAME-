import axios from "axios";
import { useContext, useState, useEffect } from "react";
import APPCONTEXT from "../../context/APPCONTEXT";
import "./board.css";
import "./rack.css";

function Board() {
  const { token } = useContext(APPCONTEXT);
  const [board, setBoard] = useState([]);
  const [rack, setRack] = useState([]);
  const [currentWord, setCurrentWord] = useState("");
  const [wordStart, setWordStart] = useState({ x: null, y: null });
  const [wordDirection, setWordDirection] = useState("right");

  const getBoard = () => {
    if(token == null){
      alert("Access token is null");
    }
    const request = axios({
      method: "GET",
      url: "http://127.0.0.1:5000/game/board",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        setBoard(res.data.board);
      })
      .catch((e) => {
        console.log("Error fetching board:", e);
      });
  };

  const getRack = () => {
    if(token == null){
      alert("Access token is null");
    }
    axios({
      method: "GET",
      url: "http://127.0.0.1:5000/game/rack",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        setRack(res.data.player_tiles);
      })
      .catch((e) => {
        console.log("Error fetching rack:", e);
      });
  };

  useEffect(() => {
    getBoard();
    getRack();
  }, []);

  const makeMove = (x, y, word, direction) => {
    if(token == null){
      alert("Access token is null");
    }

    axios({
      method: "PUT",
      url: "http://127.0.0.1:5000/game/make-move",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      data: {
        direction,
        x: parseInt(x, 10),
        y: parseInt(y, 10),
        word,
      },
    })
      .then((res) => {
        if (res.data.board) {
          setBoard(res.data.board);
        }
        alert(res.data.message);
      })
      .catch((e) => {
        console.error("Error making move:", e.response ? e.response.data : e.message);
        alert(`Error making move: ${e.response ? e.response.data.message : e.message}`);
      });
  };

  const handleDrop = (x, y, letter) => {
    if(currentWord === "") {
      setWordStart({ x, y });
    }

    setCurrentWord((prev) => prev + letter);

    updateCell(x, y, letter);
  };

  const updateCell = (x, y, letter) => {
    board[y][x] = letter;
  }

  const finalizeWord = () => {
    if (wordStart.x !== null && wordStart.y !== null && currentWord !== "") {
      makeMove(wordStart.x, wordStart.y, currentWord, wordDirection);
      setCurrentWord("");
      setWordStart({ x: null, y: null });
    } else {
      alert("Word is not valid");
    }
  };

  return (
    <div className="container">
      <div className="board">
        {board.map((row, i) => (
          <Row key={i} r={i} row={row} handleDrop={handleDrop} />
        ))}
      </div>
      <Rack tiles={rack} />
      {currentWord && (
        <div style={{ marginTop: "20px" }}>
          <p>Current Word: {currentWord}</p>
          <button onClick={finalizeWord}>Place Word</button>
        </div>
      )}
    </div>
  );
}

function Row(props) {
  const { row = [], r = 0, handleDrop = () => {} } = props;

  return (
    <div style={{ display: "flex" }}>
      {row.map((col, i) => (
        <div
          className="cell"
          key={i}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            const letter = e.dataTransfer.getData('text/plain');
            handleDrop(i, r, letter);
          }}
        >
          <Col value={col} />
        </div>
      ))}
    </div>
  );
}

function Col(props) {
  const { value } = props;

  return (
    <span style={{ fontSize: "20px" }}>
      {value}
    </span>
  );
}

function Rack(props) {
  const { tiles } = props;

  return (
    <div className="rack">
      {tiles.map((tile, index) => (
        <Tile key={index} letter={tile} />
      ))}
    </div>
  );
}

function Tile(props) {
  const { letter } = props;

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
}

export default Board;
