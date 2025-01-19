import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [companyName, setCompanyName] = useState("");
  const [result, setResult] = useState("");

  const chimata__smp__backend = async (e:any) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://127.0.0.1:8000/", {
        name: companyName,
      });
      setResult(response.data.message);
      console.log(response.data.azienda)
    } catch (error) {
      console.error("Errore nella richiesta:", error);
      setResult("C'è stato un errore durante il recupero dei dati");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Sentiment analysis previsione del mercato</h1>

      <form onSubmit={chimata__smp__backend}>
        <div>
          <label htmlFor="nomeAzienda">Nome azienda: </label>
          <input
            type="text"
            id="nomeAzienda"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="Nome azienda"
            style={{ marginLeft: "10px", padding: "5px" }}
          />
        </div>
        <button type="submit" style={{ marginTop: "10px", padding: "5px 10px" }}>
          Fetch Data
        </button>
      </form>

      <div style={{ marginTop: "20px" }}>
        <h2>Result:</h2>
        <p>{result || "nessun risultato ancora"}</p>
      </div>
    </div>
  );
};

export default App;
