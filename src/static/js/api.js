let bandwidthChart = null;
let packetLossChart = null;

function updateTrafficData() {
    axios.get('/network/get')
        .then(response => {
            const data = response.data.reverse();

            updateChart(bandwidthChart, 'bandwidthChart', 'Ancho de Banda (Mbps)', data, 'bandwidth', 'transmitted_data', 'received_data');

            updateChart(packetLossChart, 'packetLossChart', 'Pérdida de Paquetes (%)', data, 'packet_loss', 'transmitted_packets', 'lost_packets', 'Pérdida de Paquetes (%)');
        })
        .catch(error => {
            console.error('Error fetching traffic data:', error);
        });
}

function simulateTraffic() {
    axios.post('/network/create')
        .then(response => {
            console.log(response.data.message);
            updateTrafficData();
        })
        .catch(error => {
            console.error('Error simulating traffic:', error);
        });
}

function updateChart(chart, chartId, label, data, primaryMetric, secondaryMetric1, secondaryMetric2, title='') {
    const canvas = document.getElementById(chartId);

    if (canvas) {
        const ctx = document.getElementById(chartId).getContext('2d');

        if (!ctx) {
            console.error(`Error getting context for ${chartId}`);
            return;
        }
        
        if (chart) {
            // Destruir el gráfico existente si existe
            chart.destroy();
        }

        // Extraer las horas correspondientes a cada dato
        const timestamps = data.map(item => {
            const date = new Date(item.timestamp * 1000);
            const hours = date.getHours();
            const minutes = date.getMinutes();
            const seconds = date.getSeconds();
            return `${hours}:${minutes}:${seconds}`;
        });

        const newchart = new Chart(ctx, {
            type: 'line',
            data: {
                // labels: Array.from({ length: data.length }, (_, i) => i + 1),
                labels: timestamps,
                datasets: [
                    {
                        label: label,
                        data: data.map(item => item[primaryMetric]),
                        borderColor: chartId === 'bandwidthChart' ? '#3498db' : '#e74c3c',
                        borderWidth: 2,
                        fill: false,
                    },
                    {
                        label: 'Transmitidos',
                        data: data.map(item => item[secondaryMetric1]),
                        borderColor: '#2ecc71',
                        borderWidth: 2,
                        fill: false,
                    },
                    {
                        label: 'Recibidos',
                        data: data.map(item => item[secondaryMetric2]),
                        borderColor: '#f39c12',
                        borderWidth: 2,
                        fill: false,
                    },
                ],
            },
            options: {
                hover: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    x: {
                        ticks: {
                            autoSkip: true,
                            maxTicksLimit: 10,
                            color: 'white',
                        },
                        title: {
                            color: 'white',
                            display: true,
                            text: 'Hora',
                        }
                    },
                    y: {
                        ticks: {
                            color: 'white',
                        },
                        title: {
                            color: 'white',
                            display: true,
                            text: 'label',
                        }
                    },
                },
                maintainAspectRatio: false,
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: title,
                        color: 'white',
                    },
                    legend: {
                        position: 'right',
                        labels: {
                            color: 'white', 
                        },
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    },
                },
            }
        });

        if (chartId === 'bandwidthChart') {
            bandwidthChart = chart;
        } else if (chartId === 'packetLossChart') {
            packetLossChart = chart;
        }
        // if (!chart) {
        // } else {
        //     chart.data.labels = Array.from({ length: data.length }, (_, i) => i + 1);
        //     chart.data.datasets[0].data = data;
        //     chart.update();
        // }
        return newchart;
    } else {
        console.error(`Error getting canvas for ${chartId}`);
    }
}

updateTrafficData();

// setInterval(updateTrafficData, 60000);

setInterval(() => {
    window.location.reload();
}, 60000)

setInterval(simulateTraffic, 30000);
