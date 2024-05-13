Chart.register(ChartDataLabels);
Chart.defaults.font.size = 14;
Chart.defaults.font.weight = 'bold' ;

var ageChart; // Declare ageChart variable outside the scope
// Fetch gender data
fetch('/php/chart_data_year.php')
    .then(response => response.json())
    .then(gender_data => {
        var ctx1 = document.getElementById('genderChart').getContext('2d');
        var genderChart = new Chart(ctx1, {
            plugins: [ChartDataLabels],
            type: 'pie',
            data: {
                labels: ['Female','Male'],
                datasets: [{
                    data: Object.values(gender_data),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(54, 162, 235, 0.5)',
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 3)',
                        'rgba(54, 162, 235, 3)',
                    ],
                    borderWidth: 3
                    
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels:{
                            font:{
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    datalabels: {
                        font:{
                        size: 14,
                         weight: 'bold'
                        },
                        formatter: (value, ctx) => {
                            const datapoints = ctx.chart.data.datasets[0].data;
                            const total = datapoints.reduce((total, datapoint) => total + datapoint, 0);                            
                            const percentage = value / total * 100  
                            return percentage.toFixed(2) + "%" + " " + "(" + value + ")" ;
                        }
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error fetching age data:', error));
  
    document.addEventListener('DOMContentLoaded', function () {
        // Fetch age data
        fetch('/php/age_data_year.php')
        .then(response => response.json())
        .then(data => {
            var male_age_data = data.male;
            var female_age_data = data.female;
    
            var ctx = document.getElementById('ageChart').getContext('2d');
    
            var maleColors = [
                'rgba(54, 162, 235, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(54, 162, 235, 0.5)'
            ];
    
            var femaleColors = [
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)'
            ];
    
            ageChart = new Chart(ctx, { // Assign ageChart here
                type: 'bar',
                data: {
                    labels: Object.keys(male_age_data),
                    datasets: [{
                        label: 'Male',
                        data: Object.values(male_age_data),
                        backgroundColor: maleColors,
                        borderColor: 'rgba(54, 162, 235, 3)',
                        borderWidth: 3
                    }, {
                        label: 'Female',
                        data: Object.values(female_age_data),
                        backgroundColor: femaleColors,
                        borderColor: 'rgba(255, 99, 132, 3)',
                        borderWidth: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 50 ,
                            ticks: {
                                stepSize: 10
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                },
                            }
                        },
                        datalabels: {
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    }
                }
            });
        });
    });
                    // Function to update chart data based on age range

// Fetch time data      
fetch('/php/time_data_year.php')
    .then(response => response.json())
    .then(time_data => {
        const timeIntervals = Object.keys(time_data);
        const customerCounts = Object.values(time_data);

        // Get canvas element
        const ctx = document.getElementById('timeChart').getContext('2d');

        // Create time chart
        const timeChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: timeIntervals,
                datasets: [{
                    label: 'Number of Customers',
                    data: customerCounts,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)', // Adjust color as needed
                    borderColor: 'rgba(54, 162, 235, 1)', // Adjust color as needed
                    borderWidth: 2  
                }]
            },
            options: {
                scales: {
                    y: {
                        min: 0,
                        max: 50,
                        ticks: {
                            stepSize: 10
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Number of Customers: ' + context.parsed.y;
                            }
                        }
                    }
                }
            }
        });

        // Update information div
        const infoDiv = document.getElementById('timeInfo');
        infoDiv.innerHTML = `<p><strong>Total Customers:</strong> ${customerCounts.reduce((a, b) => a + b, 0)}</p>`;
    })
    .catch(error => console.error('Error fetching time data:', error));

    document.addEventListener('DOMContentLoaded', function () {
        // Fetch the data from PHP script
        fetch("/php/hour_data_year.php")
            .then(response => response.json())
            .then(data => {
                // Extract labels and values from the received data
                const labels = Object.keys(data);
                const values = Object.values(data);
    
                // Create a line chart
                var ctx = document.getElementById('MyChart').getContext('2d');
                var MyChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Monthly Data',
                            data: values,
                            fill: false,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                               min: 0 ,
                               max: 50 ,
                               ticks: {
                                stepSize: 10
                               }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching data:', error));
    });