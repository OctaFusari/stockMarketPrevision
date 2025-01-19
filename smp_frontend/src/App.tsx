import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [nomeAzienda, setNomeAzienda] = useState("");
  const [modelType, setTipoModello] = useState("");
  const [result, setResult] = useState({
    previsione: "",
    accuratezza: "",
    errore: "",
  });
  const [loading, setLoading] = useState(false);

  const handleModelChange = (event: any) => {
    setTipoModello(event.target.value);
  };

  const chimata__smp__backend = async (e: any) => {
    e.preventDefault();
    setLoading(true);

    try {
      await axios
        .post("http://127.0.0.1:8000/", {
          name: nomeAzienda,
          modello: modelType,
        })
        .then((response) => {
          setLoading(false);

          setResult({
            previsione: response.data.message.previsione,
            accuratezza: response.data.message.accuratezza,
            errore: "",
          });
          console.log(response.data.message);
        });
    } catch (error) {
      console.error("Errore nella richiesta:", error);
      setResult({
        previsione: "",
        accuratezza: "",
        errore: "C'è stato un errore durante il recupero dei dati",
      });
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <div>
        <h1>SMP</h1>
        <p>
          Previsione dell'andamento delle aziende attraverso la sentiment
          analysis
        </p>
      </div>

      <div className="grid__centrale">
        <div className="container">
          <form onSubmit={chimata__smp__backend}>
            <div>
              <h2>
                <label htmlFor="nomeAzienda">CIK azienda: </label>
              </h2>
              <input
                type="text"
                id="nomeAzienda"
                value={nomeAzienda}
                onChange={(e) => setNomeAzienda(e.target.value)}
                placeholder="Nome azienda"
                style={{ marginLeft: "10px", padding: "5px" }}
              />
            </div>
            <h2>Seleziona il tipo di modello</h2>

            <div>
              <label>
                <input
                  type="radio"
                  value="svc__OBJ"
                  checked={modelType === "svc__OBJ"}
                  onChange={handleModelChange}
                />
                Modello basato su SVC
              </label>
            </div>

            <div>
              <label>
                <input
                  type="radio"
                  value="rf__OBJ"
                  checked={modelType === "rf__OBJ"}
                  onChange={handleModelChange}
                />
                Modello basato su Random Forest
              </label>
            </div>
            <button
              type="submit"
              style={{ marginTop: "10px", padding: "5px 10px" }}
            >
              Fai previsione
            </button>
          </form>
        </div>
        {loading ? (
          <div className="spinner"></div> // Mostra lo spinner mentre carica
        ) : (
          <div className="container">
            <h2>Risultato</h2>
            <p>{result.previsione || "nessun risultato ancora"}</p>
            <h2>Accuratezza del modello</h2>
            <p>{result.accuratezza || "nessun risultato ancora"}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
