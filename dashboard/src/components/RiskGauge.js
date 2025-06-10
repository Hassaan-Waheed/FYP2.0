import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const RiskGauge = ({ score, risk }) => {
  const data = {
    datasets: [{
      data: [score, 1 - score],
      backgroundColor: [
        risk === 'high' ? '#ff4444' : risk === 'medium' ? '#ffbb33' : '#00C851',
        '#e9ecef'
      ],
      borderWidth: 0
    }]
  };

  const options = {
    cutout: '80%',
    rotation: -90,
    circumference: 180,
    plugins: {
      legend: {
        display: false
      }
    }
  };

  return (
    <div style={{ width: '200px', height: '100px', position: 'relative' }}>
      <Doughnut data={data} options={options} />
      <div style={{
        position: 'absolute',
        bottom: '10px',
        width: '100%',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '24px', fontWeight: 'bold' }}>
          {Math.round(score * 100)}%
        </div>
        <div style={{ fontSize: '14px', color: '#666' }}>
          {risk.toUpperCase()} RISK
        </div>
      </div>
    </div>
  );
};

export default RiskGauge; 