import { useState, useContext } from "react";
import axios from "axios";

import ErrorPanel from "../../components/ErrorPanel";

import APPCONTEXT from "../../context/APPCONTEXT";


import { useNavigate } from "react-router-dom";

function SignUp() {
  const [alias, setAlias] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [Errormessage, setErrormessage] = useState(null);

  const { setUser, setToken } = useContext(APPCONTEXT);

  const navigate = useNavigate();

  const handleSubmit = () => {
    axios({
      method: "POST",
      url: "http://127.0.0.1:5000/signup",
      data: {
        username: alias,
        email: email,
        password: password,
      },
    })
      .then((res) => {
        const data = res.data;
        setUser(data.user || null);
        setToken(data.token || null);
        setErrormessage(null);
        navigate("/");
      })
      .catch((e) => {
        setErrormessage(e?.response?.data?.message || "Try Again");
      });
  };

  return (
    <div className=" c_screen">
      <div className="w3-panel w3-teal">
        <h3>SIGN UP</h3>
      </div>
      <div
        className=""
        style={{ display: "flex", justifyContent: "center", width: "100%" }}
      >
        <div
          className="w3-card-4 w3-padding"
          style={{
            width: "30%",
          }}
        >
          <label className="w3-text-blue">
            <b>Alias</b>
          </label>
          <input
            className="w3-input w3-border"
            type="text"
            onChange={(e) => setAlias(e.target.value)}
          />

          <label className="w3-text-blue">
            <b>Email</b>
          </label>
          <input
            className="w3-input w3-border"
            type="text"
            onChange={(e) => setEmail(e.target.value)}
          />

          <label className="w3-text-blue">
            <b>Password</b>
          </label>
          <input
            className="w3-input w3-border"
            type="password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            onClick={handleSubmit}
            style={{ marginTop: "10px" }}
            className="w3-btn w3-blue"
          >
            Sign Up
          </button>
        </div>
      </div>

      <ErrorPanel Errormessage={Errormessage} />
    </div>
  );
}

export default SignUp;