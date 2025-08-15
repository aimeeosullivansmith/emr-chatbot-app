import './App.css';
import React, { useEffect, useState } from "react";

function App() {
  const [tester, setTester] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/hello") 
      .then((res) => res.json())
      .then((data) => {
      console.log("Data from backend:", data);
      setTester(data.tester);
    })
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="App">
      <h2>{tester}</h2>
      <h3>hello react</h3>
    </div>
  );
}

export default App;
