
let transaction_types = {
    buy: 1,
    sell: 0,
};

let asset = {
    name: '',
    type: '',
    quantity: 1
};

function prepare_transaction(transaction) {

    let url = transaction === transaction_types.buy?
        '/game/ajax/buy/':'/game/ajax/sell/';


    divs_hidden_by_default([
        $("#quantity-form"),
        $("#accept-form"),
        $("#trans-status"),
    ]);

    load_action_listener();

    $("#send-quantity").click(function () {
        //on quantity select
        asset.quantity = $("#quantity").val();
        console.log("send-quantity");
        show_information_form(asset, populate_accept_form, transaction)
    });

    $("#cancel-quantity").click(function () {
        //on cancel quantity form
        $("#quantity-form").hide(400);
        if (transaction_types.buy === transaction)
            reload_all();
    });

    $("#accept-transaction").click(function () {
        show_transaction_status();
        start_transaction(url, asset.name, asset.quantity, asset.type);
    });

    $("#cancel-transaction").click(function () {
        $("#accept-form").stop(true).hide(400);
        $("#quantity-form").show(500);
    });

    $("#accept-transaction-success").click(function () {
        if (transaction_types.buy === transaction)
            reload_all();

        $("#trans-status").hide(400);
    });
}

function load_action_listener() {
    let action = $(".action");
    action.unbind();
    action.click(function () {
        asset.name = $(this).attr("id");
        asset.type = $(this).attr("type");
        $("#quantity-form").show(500);
        //pause reload
        clearInterval(reload);
    });
}

