function prepare_token() {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}


function divs_hidden_by_default(divs) {
    $.each(divs, function () {
        this.hide();
    })
}

function populate_accept_form(div, asset_quote, quantity, transaction) {
    let price = transaction === transaction_types.buy ? asset_quote.buy : asset_quote.sell;

    asset.buy = asset_quote.buy;
    asset.sell = asset_quote.sell;

    div.find("#name").html(asset_quote.name);
    div.find("#price").html("$  " + price);
    div.find("#total").html("$  " + price * quantity)
}

function populate_response_form(type, div, data) {
    let status = div.find("#status");
    let label = div.find("label");
    status.html(data.message);
    if (data.error) {
        label.html("We are very sorry but an error ocurred");
        status.css('color', '#CD0000');
        status.css('font-weight', 'bold');
        status.css('font-size', '23px');
    } else {
        let trans = type === transaction_types.buy ?
            'bought' : 'sold';

        let price = type === transaction_types.buy ?
            asset.buy : asset.sell;

        label.html(
            `You have ${trans} ${asset.quantity} ${asset.name} at ${price} each!`
        );

        status.css('color', 'green');
        status.css('font-weight', 'bold');
        status.css('font-weight', '23px');
    }
    div.find("#loading").hide();
    $("#accept-t").show(500);
}

function prepare_input_nicenumber() {
    $('input[type="number"]').niceNumber({
        autoSize: false,
        step: 0.01
    })
        .keydown(function (event) {


            if (event.shiftKey == true) {
                event.preventDefault();
            }

            if ((event.keyCode >= 48 && event.keyCode <= 57) ||
                (event.keyCode >= 96 && event.keyCode <= 105) ||
                event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 37 ||
                event.keyCode == 39 || event.keyCode == 46 || event.keyCode == 190) {

            } else {
                event.preventDefault();
            }

            if ($(this).val().indexOf('.') !== -1 && event.keyCode == 190)
                event.preventDefault();
            //if a decimal has been added, disable the "."-button

        });
}

let window_close_timeout = null;
let timer_interval = null;

function stopTimer() {
    clearInterval(timer_interval);
    setTimeout(
        function () {
            $(".timer").find("p").html(5);
        }, 1000
    )
}

function show_information_form(asset, onsuccess, transaction) {
    $("#quantity-form").hide(400);
    $("#accept-form").show(500);

    if (window_close_timeout != null) {
        clearTimeout(window_close_timeout);
    }
    window_close_timeout = setTimeout(
        (function () {
            $("#accept-form").hide(400);
            if (transaction_types.buy === transaction)
                reload_all();
            stopTimer();
        }), 5000
    );

    timer_interval = setInterval(
        function () {
            let timer = $(".timer").find("p");
            let old_num = parseInt(timer.html());
            timer.html(old_num - 1);
        }, 900
    );


    $.ajax({
        url: '/game/ajax/quote/' + asset.name,
        success: function (data) {
            onsuccess($("#accept-form"), data, asset.quantity, transaction)
        },
        error: function (jqXHR, status, errorThrown) {
            $("#accept-form").find("label")
                .html("This asset is not available anymore")
                .css('color', 'red');
        }
    });
}

function show_transaction_status() {
    $("#accept-form").stop(true).hide(400);
    $("#trans-status").show(500).find("#accept-t").hide(0);
}

function start_transaction(transaction, name, quantity, type) {

    let url = transaction === transaction_types.buy ?
        '/game/ajax/buy/' : '/game/ajax/sell/';

    $.ajax({
        url: url,
        type: 'post',
        data: {
            'name': name,
            'quantity': quantity,
            'type': type,
        },
        success: function (data) {
            populate_response_form(transaction, $("#trans-status"), data);
        },
        error: function (jqXHR, status, errorThrown) {
            populate_response_form(transaction, $("#trans-status"), {
                'error': true,
                'message': status
            });
        }
    });
}


