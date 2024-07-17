import { useState } from "react";
import { Route, Routes, BrowserRouter } from "react-router-dom";
import SignUp from "./APP/Pages/SignUp";
import Login from "./APP/Pages/Login";
import Game from "./APP/Pages/Game";
import NotFound from "./APP/Pages/NotFound";
import APPCONTEXT from "./APP/Context/APPCONTEXT";

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
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
       </APPCONTEXT.Provider>
    );
  }
  
  export default APP;