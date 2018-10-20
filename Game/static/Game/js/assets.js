function reload_all() {
    setInterval(function () {
        $.ajax({
            url: '',
            success: function (data) {
                console.log("ajax success");
                $(".dinamic-row").remove();

                $.each(data.assets, function (a) {
                    console.log(a);

                    var data = '<tr class="dinamic-row">';
                    data += `<td><a class="action" id="${this.name}" type="${this.type}" href="#">BUY</a></td>`;
                    data += `<td id="name" >${this.name}</td>`;
                    data += `<td id="buy" >$ ${this.buy}</td>`;
                    data += `<td id="sell">$ ${this.sell}</td>`;
                    data += `<td> ${this.type} </td>`;
                    data += `<td><a class="history" href="/game/history/${this.name} ">History</a></td>`;
                    $("#dinamic-table").append(data);
                })
            },
        });
    }, 5000);
}

function reload_prices() {
    $('.dinamic-info').each(function () {
        reload($(this))
    });
}

function reload(info) {
    $.ajax({
        url: '/game/ajax/quote/' + info.find("#name").html(),
        success: function (data) {
            console.log(data);
            let buy = data.buy;
            let sell = data.sell;
            info.find("#buy").html("$ " + buy);
            info.find("#sell").html("$ " + sell);
            info.find(".action").show();
            info.find(".history").show();
        },
        error: function (jqXHR, status, errorThrown) {
            info.find("#buy").html(" Unavailable ");
            info.find("#sell").html(" Unavailable ");
            info.find(".action").hide(300);
            info.find(".history").hide(300);
        },
    });
}

