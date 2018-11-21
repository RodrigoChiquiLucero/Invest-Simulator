function populate_chart(data, thres, price, actual_price) {
    const container = document.getElementById("myChart");

    let raw_data = data.replace(/'/g, '"');
    let quantiles = JSON.parse(raw_data || '{}');

    let avg = quantiles[price]['avg'].toFixed(3);
    let first = quantiles[price]['first'].toFixed(3);
    let third = quantiles[price]['third'].toFixed(3);

    let ctx = container.getContext('2d');
    let myChart = new Chart.Scatter(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Threshold',
                data: [{x: thres, y: thres}],
                backgtoFixedColor:
                    'rgba(  255,    99,     132,    0.2)',
                borderColor:
                    'rgba(  255,    99,     132,    1)',
                borderWidth: 1,
                fill: false,
                tension: 0,
                showLine: true
            }, {
                label: price + ' average price',
                data: [{x: avg, y: avg}],
                backgtoFixedColor:
                    'rgba(  50,  0,     255,    0.2)',
                borderColor:
                    'rgba(  50,  0,     255,    1)',
                borderWidth: 1
            }, {
                label: price + ' price first quartile',
                data: [{x: first, y: first}],
                backgtoFixedColor:
                    'rgba(  132,  99,     255,    0.2)',
                borderColor:
                    'rgba(  132,  99,     255,    1)',
                borderWidth: 1
            }, {
                label: price + ' price third quartile',
                data: [{x: third, y: third}],
                backgtoFixedColor:
                    'rgba(  132,  99,     255,    0.2)',
                borderColor:
                    'rgba(  132,  99,     255,    1)',
                borderWidth: 1
            }, {
                label: 'Actual price',
                data: [{x: actual_price, y: actual_price}],
                backgtoFixedColor:
                    'rgba( 50 , 255, 0,    0.2)',
                borderColor:
                    'rgba( 50, 255, 0,    1)',
                borderWidth: 1
            }]
        },
        options: {
            tooltips: {
                callbacks: {
                    label: function (tooltipItems, data) {
                        let label = data.datasets[tooltipItems.datasetIndex].label;
                        return label + " - $ " + tooltipItems.xLabel.toString();
                    }
                }
            },
            title: {
                display: true,
                text: 'Asset stats'
            },
        }
    });
}
