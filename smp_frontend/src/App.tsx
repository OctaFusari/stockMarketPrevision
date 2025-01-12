
import './App.css'
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App: React.FC = () => {
    const [data, setData] = useState("");

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/")
            .then(response => setData(response.data.message))
            .catch(error => console.error(error));
    }, []);

    return <h1>{data}</h1>;
};

export default App;
