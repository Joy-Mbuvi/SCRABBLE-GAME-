import APPCONTEXT from "../../Context/APPCONTEXT";
import { useContext, useState, useEffect } from "react";

import axios from "axios";

import { useNavigate } from "react-router-dom";

import Board from "./Board";

function Game() {
  const { user, token } = useContext(APPCONTEXT);
  const navigate = useNavigate();

  const [board, setBoard] = useState([]);

  console.log(board);

  useEffect(() => {
    if (!user || !token) {
      navigate("/");
      return;
    }
    getboard();
  }, []);

  const getboard = () => {
    axios({
      method: "GET",
      url: "http://127.0.0.1:9000/game/board",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        setBoard(res?.data?.board || []);
      })
      .catch((err) => {
        if (!user || !token) {
          navigate("/");
          return;
        }
      });
  };

  return (
    <div className=" c_screen">
      <div className="w3-panel w3-pale-green">
        <div
          className=" "
          style={{
            width: "100%",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div>
            <p>Welcome Player: {user?.alias} </p>
          </div>
          <div>
            <button className="w3-btn w3-round w3-pink ">Logout</button>
            <button className="w3-btn w3-round w3-green w3-margin-left">
              New Game
            </button>
          </div>
        </div>
      </div>
      <div style={{ display: "flex", justifyContent: "center" }}>
        <Board board={board} setBoard={setBoard} getboard={getboard} />
      </div>
    </div>
  );
}

export default Game;