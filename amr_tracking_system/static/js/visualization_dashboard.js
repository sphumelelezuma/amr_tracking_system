document.addEventListener("DOMContentLoaded", function () {
    // Retrieve the hidden inputs with the JSON data
    const resistanceLabels = JSON.parse(document.getElementById('resistanceLabels').value);
    const resistanceData = JSON.parse(document.getElementById('resistanceData').value);

    // Get the canvas context for the chart
    const ctx = document.getElementById('resistanceChart').getContext('2d');

    // Create the chart using Chart.js
    const resistanceChart = new Chart(ctx, {
        type: 'bar',  // Change chart type if needed
        data: {
            labels: resistanceLabels,
            datasets: [{
                label: 'Resistance Percentage',
                data: resistanceData,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
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
});
