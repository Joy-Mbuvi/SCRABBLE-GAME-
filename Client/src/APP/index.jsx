
import { Route, Routes, BrowserRouter } from "react-router-dom";
import { useState } from "react";
import SignUp from "./Pages/SignUp";
import Login from "./Pages/Login";
import Game from "./Pages/Game";
import APPCONTEXT from "./context/APPCONTEXT";



function APP() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  return (
    <APPCONTEXT.Provider value={{ user, setUser, token, setToken }}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/sign-up" element={<SignUp />} />
          <Route path="/game" element={<Game />} />
        </Routes>
      </BrowserRouter>
    </APPCONTEXT.Provider>
  );
}

export default APP;