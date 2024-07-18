import { useState, useContext } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import ErrorPanel from "../../components/ErrorPanel";
import APPCONTEXT from "../../context/APPCONTEXT";




function Login() {
    const [email,setEmail] =useState("");
    const [password,setPassword] =useState("");
    const [errormessage,setErrormessage] =useState(null);

    const { setUser, setToken } = useContext(APPCONTEXT);
    const navigate = useNavigate();

    const handleSubmit = () => {
        console.log(email,password);
        
        axios({
         method: "POST",
         url: "http://127.0.0.1:5000/login",
         data: {
            email: email,
            password: password,
         },   
        })
        .then((res) => {
            const data = res?.data;
            setToken(data?.token || null);
            setUser(data?.user || null);
            setErrormessage(null);
            navigate("/game");
        })
        .catch((e) => {
            setErrormessage(e?.response?.data?.message || " Try Again")  
        })
    };
    return(
<div className=" c_screen">
    <div className="w3-panel w3-deep-orange">
        <h3>LOGIN</h3>
    </div> 
    <div style={{display: "flex",justifyContent: "center",width:"100%"}}>
        <div 
            className="w3-card-4 w3-padding"
            style={{
                width: "20%"
            }}
        >
            <label className="w3-text-blue"><b>Email</b></label>
            <input className="w3-input w3-border" 
                   type="text" 
                   onChange={(e)=> setEmail(e.target.value)}
            
            />
 
            <label className="w3-text-blue"><b>password</b></label>
            <input className="w3-input w3-border" 
                   type="password"
                   onChange={(e)=> setPassword(e.target.value)}
                    />

            <button 
            onClick={handleSubmit}
            style={{marginTop: "10px"}} className="w3-btn w3-blue">Login</button>
        </div>
    </div>
     <ErrorPanel errormessage={errormessage} />  
</div>
 );
}

export default Login;