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

function populate_accept_form(div, asset, quantity, transaction) {
    let price = transaction === transaction_types.buy? asset.buy: asset.sell;

    div.find("#name").html(asset.name);
    div.find("#price").html("$  " + price);
    div.find("#total").html("$  " + price * quantity)
}

function populate_response_form(div, data) {
    let status = div.find("#status");
    let label = div.find("label");
    status.html(data.message);
    if (data.error) {
        label.html("We are very sorry but an error ocurred");
        status.css('color', 'red');
    } else {
        label.html("Transaction successfull!");
        status.css('color', 'green');
    }
    div.find("#loading").hide();
    $("#accept-t").show(500);
}

function prepare_input_nicenumber() {
    $('input[type="number"]').niceNumber()
        .on("keypress", function (e) {
            switch (e.key) {
                case "1":
                case "2":
                case "3":
                case "4":
                case "5":
                case "6":
                case "7":
                case "8":
                case "9":
                case "0":
                case "Backspace":
                    return true;

                default:
                    return false;
            }
        });
}

let window_close_timeout = null;
function show_information_form(asset, onsuccess, transaction) {
    $("#quantity-form").hide(400);
    $("#accept-form").show(500)

    if (window_close_timeout != null) {
        clearTimeout(window_close_timeout);
    }
    window_close_timeout = setTimeout(
        (function () {
            $("#accept-form").hide(400);
            if (transaction_types.buy === transaction)
                reload_all();
        }), 5000
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

function start_transaction(url, name, quantity, type) {
    $.ajax({
        url: url,
        type: 'post',
        data: {
            'name': name,
            'quantity': quantity,
            'type': type,
        },
        success: function (data) {
            populate_response_form($("#trans-status"), data);
        },
        error: function (jqXHR, status, errorThrown) {
            populate_response_form($("#trans-status"), {
                'error': true,
                'message': status
            });
        }
    });
}


