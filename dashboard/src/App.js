import React, { useState } from 'react';
import RiskGauge from './components/RiskGauge';
import axios from 'axios';

function App() {
  const [ticker, setTicker] = useState('');
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(`http://localhost:8000/predict/${ticker}`);
      setPrediction(response.data);
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }
  };

  return (
    <div className="App">
      <h1>Crypto Investment Analysis</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="Enter crypto ticker"
        />
        <button type="submit">Analyze</button>
      </form>
      {prediction && (
        <div>
          <h2>Analysis Results</h2>
          <RiskGauge score={prediction.score} risk={prediction.risk} />
          <div>
            <h3>Detailed Predictions</h3>
            <pre>{JSON.stringify(prediction.predictions, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default App; 