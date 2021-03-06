let reload = null;

//REALOAD ALL ASSETS INSIDE TABLE
function reload_all() {
    if(reload !== null) {
        clearInterval(reload)
    }

    reload = setInterval(function () {
        reload_assets_for_table($("#dinamic-table"));
    }, 10000);
}

function reload_assets_for_table(table) {
    $.ajax({
        url: '',
        success: function (data) {
            $(".dinamic-row").remove();
            $("#prepare_transaction").remove();

            console.log("Info updated");

            $.each(data.assets, function (a) {
                var data = `<tr class="dinamic-row">
                                <td id="name">${ this.name }</td>
                                <td id="type"> ${ this.type }</td>
                                <td id="sell">$ ${ this.sell }</td>
                                <td id="buy">$ ${ this.buy } </td>
                                <td><a class="action w3-button w3-green w3-round-large " id="${ this.name }" type="${ this.type }" href="#">
                                    <i class="fas fa-dollar-sign"></i> Buy
                                </a></td>
                                <td><a class="action w3-button w3-green w3-round-large " href="/game/history/${ this.name } ">
                                    <i class="fas fa-history"></i> History
                                </a></td>`;
                table.append(data);
            });
            load_action_listener();
        },
    });
}

//RELOAD PRICES FOR YOUR WALLET
function reload_prices() {
    setInterval(function () {
        $('.dinamic-row').each(function () {
            reload_prices_for_row($(this))
        });
    }, 10000);
}

function reload_prices_for_row(row) {
    $.ajax({
        url: '/game/ajax/quote/' + row.find("#name").html(),
        success: function (data) {

            console.log("Info updated");

            let buy = data.buy;
            let sell = data.sell;
            row.find("#buy").html("$ " + buy);
            row.find("#sell").html("$ " + sell);
            row.find(".action").show();
            row.find(".history").show();
        },
        error: function (jqXHR, status, errorThrown) {
            row.find("#buy").html(" Unavailable ");
            row.find("#sell").html(" Unavailable ");
            row.find(".action").hide(300);
            row.find(".history").hide(300);
        },
    });
}

