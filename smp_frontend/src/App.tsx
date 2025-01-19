
import './App.css'
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App: React.FC = () => {
    let [data, setData] = useState("");
    let datBack:any

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/")
            .then(response => {
                datBack = response.data.message
                setData(response.data.message)
                console.log(response.data.message)
            })
            .catch(error => console.error(error));
    }, []);

    return (
        <div>
            {/* <h1>Dati raccolti dalla sentiment analysis</h1>
            <h2>Dati positivi: {data[0]}</h2>
            <h2>Dati negativi: {data[1]}</h2> */}
        </div>
    );
};

export default App;



                