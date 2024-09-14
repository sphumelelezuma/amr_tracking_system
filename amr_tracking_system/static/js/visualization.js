// Fetch data from the API endpoint
fetch('/api/visualization_data/')
    .then(response => response.json())
    .then(data => {
        // Extract data for charts
        const resistanceLabels = data.resistance_labels;
        const resistanceData = data.resistance_data;
        const pathogenLabels = data.pathogen_labels;
        const pathogenData = data.pathogen_data;

        // Create charts with Chart.js
        createCharts(resistanceLabels, resistanceData, pathogenLabels, pathogenData);
    })
    .catch(error => console.error('Error fetching data:', error));

// Function to create charts with Chart.js
function createCharts(resistanceLabels, resistanceData, pathogenLabels, pathogenData) {
    // Bar chart for Resistance Percentage by Location
    var ctx1 = document.getElementById('resistanceChart').getContext('2d');
    var resistanceChart = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: resistanceLabels,  // Locations
            datasets: [{
                label: 'Resistance Percentage',
                data: resistanceData,  // Resistance percentages
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Bar chart for Top Pathogens with Highest Resistance
    var ctx2 = document.getElementById('topPathogensChart').getContext('2d');
    var topPathogensChart = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: pathogenLabels,  // Pathogens
            datasets: [{
                label: 'Resistance Percentage',
                data: pathogenData,  // Resistance percentages
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
