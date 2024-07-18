function Row(props) {
    const { row = [] } = props;
  
    return (
      <div style={{ display: "flex" }}>
        {row.map((col, i) => {
          return (
            <div key={i} style={{ width: "40px", height: "40px" }}>
              {col}
            </div>
          );
        })}
      </div>
    );
  }
  
  export default Row;