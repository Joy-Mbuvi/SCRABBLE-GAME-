import React from "react";
function ErrorPanel(props){
    const {errormessage = null} = props;

    if(!errormessage) {
        return null;
    }
    return(
      <div className="w3-panel w3-red">
        <h3>Error!</h3>
        <p>{errormessage}</p>
       </div>
      );    
}

export default ErrorPanel;