import axios from "axios";
import { useContext, useState, useEffect } from "react";
import APPCONTEXT from "../../context/APPCONTEXT";
import Tile from '../../components/tile'; 

function Board() {
  const { token } = useContext(APPCONTEXT);
  const [board, setBoard] = useState([]);
  const [rack, setRack] = useState([]);

  const getBoard = () => {
    axios({
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
    axios({
      method: "PUT",
      url: "http://127.0.0.1:5000/game/make-move",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      data: {
        x,
        y,
        word,
        direction,
      },
    })
      .then((res) => {
        if (res.data.board) {
          setBoard(res.data.board);
        }
        alert(res.data.message);
      })
      .catch((e) => {
        console.error("Error making move:", e);
        alert("Error making move. Please check the console for more details.");
      });
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div className="board">
        {board.map((row, i) => (
          <Row key={i} r={i} row={row} setBoard={setBoard} makeMove={makeMove} />
        ))}
      </div>
      <Rack tiles={rack} />
    </div>
  );
}

function Row(props) {
  const { row = [], r = 0, setBoard = () => {}, makeMove = () => {} } = props;

  return (
    <div style={{ display: "flex" }}>
      {row.map((col, i) => (
        <div
          className="w3-border"
          key={i}
          style={{
            width: "40px",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "40px",
            backgroundColor: "white",
            border: "1px solid black",
          }}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            const letter = e.dataTransfer.getData('text/plain');
            makeMove(i, r, letter, 'right'); // or 'down', depending on your use case
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

  if (value) {
    return (
      <span style={{ fontSize: "20px" }}>
        {value}
      </span>
    );
  }

  return null;
}

function Rack(props) {
  const { tiles } = props;
  return (
    <div className="rack" style={{ display: 'flex', marginTop: '20px' }}>
      {tiles.map((tile, index) => (
        <Tile key={index} letter={tile} />
      ))}
    </div>
  );
}

export default Board;
