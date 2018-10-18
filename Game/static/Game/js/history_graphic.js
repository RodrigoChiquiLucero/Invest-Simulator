const container = document.getElementById("myChart");
const raw_data = container.getAttribute("data-js-vars").replace(/'/g, '"');
const data = JSON.parse(raw_data || '{}');

let dates = data.map(function(item) {
    return item.day;
});
let buys = data.map(function(item) {
    return item.buy;
});
let sells = data.map(function(item) {
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
            backgroundColor: [
                'rgba(  255,    99,     132,    0.2)',
                'rgba(  54,     162,    235,    0.2)',
                'rgba(  255,    206,    86,     0.2)',
                'rgba(  75,     192,    192,    0.2)',
                'rgba(  153,    102,    255,    0.2)',
                'rgba(  255,    159,    64,     0.2)'
            ],
            borderColor: [
                'rgba(  255,    99,     132,    1)',
                'rgba(  54,     162,    235,    1)',
                'rgba(  255,    206,    86,     1)',
                'rgba(  75,     192,    192,    1)',
                'rgba(  153,    102,    255,    1)',
            ],
            borderWidth: 1
        },{
            label: 'Sell price',
            data: sells,
            backgroundColor: [
                'rgba(  132,  99,     255,    0.2)',
                'rgba(  235,  162,    54,     0.2)',
                'rgba(  86,   206,    255,    0.2)',
                'rgba(  192,  192,    75,     0.2)',
                'rgba(  255,  102,    153,    0.2)',
                'rgba(  64,   159,    255,    0.2)'
            ],
            borderColor: [
                'rgba(  132,  99,     255,    1)',
                'rgba(  235,  162,    54,     1)',
                'rgba(  86,   206,    255,    1)',
                'rgba(  192,  192,    75,     1)',
                'rgba(  255,  102,    153,    1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
