const container = document.getElementById("myChart");
const raw_data = container.getAttribute("data-js-vars").replace(/'/g, '"');
const data = JSON.parse(raw_data || '{}');

let dates = data.map(function (item) {
    return item.day;
});
let buys = data.map(function (item) {
    return item.buy;
});
let sells = data.map(function (item) {
    return item.sell;
});

let ctx = document.getElementById("myChart").getContext('2d');
let myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: dates,
        datasets: [{
            label: 'Buy price',
            data: buys,
            backgroundColor:
                'rgba(  255,    99,     132,    0.2)',
            borderColor:
                'rgba(  255,    99,     132,    1)',
            borderWidth: 1
        }, {
            label: 'Sell price',
            data: sells,
            backgroundColor:
                'rgba(  132,  99,     255,    0.2)',
            borderColor:
                'rgba(  132,  99,     255,    1)',
            borderWidth: 1
        }]
    },
    options: {
        tooltips: {
            callbacks: {
                label: function (tooltipItems, data) {
                    return "$ " + tooltipItems.yLabel.toString();
                }
            }
        },
        title: {
            display: true,
            text: 'Time / price graphic'
        }, scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: "Price"
                },
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
