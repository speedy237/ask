import React, { useEffect, useRef } from 'react';
import {
  Chart,
  BarController, // Import the BarController
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js';

// Register necessary components for a bar chart
Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const BarChartComponent = ({ xmlFilePath }) => { // Accept xmlFilePath as a prop
  const chartRef = useRef(null); // Reference to the canvas element
  const chartInstanceRef = useRef(null); // Reference to the chart instance

  useEffect(() => {
    // Fetch and parse XML data
    fetch(xmlFilePath) // Use the provided file path
      .then((response) => response.text())
      .then((xmlData) => {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xmlData, 'application/xml');

        // Extract labels and data
        const labels = Array.from(xmlDoc.getElementsByTagName('label')).map((el) => el.textContent);
        const data = Array.from(xmlDoc.getElementsByTagName('value')).map((el) =>
          parseInt(el.textContent, 10)
        );

        // Destroy the previous chart instance if it exists
        if (chartInstanceRef.current) {
          chartInstanceRef.current.destroy();
        }

        // Create a new chart instance
        const ctx = chartRef.current.getContext('2d');
        chartInstanceRef.current = new Chart(ctx, {
          type: 'bar', // Specify the chart type as "bar"
          data: {
            labels: labels,
            datasets: [
              {
                label: 'Dataset',
                data: data,
                backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                ],
                borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                ],
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'top',
              },
              tooltip: {
                enabled: true,
              },
            },
            scales: {
              x: {
                beginAtZero: true,
              },
              y: {
                beginAtZero: true,
              },
            },
          },
        });
      });

    // Cleanup the chart when the component is unmounted
    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
      }
    };
  }, [xmlFilePath]); // Add xmlFilePath to the dependency array

  return <canvas ref={chartRef}></canvas>;
};

export default BarChartComponent;
