
let transaction_types = {
    buy: 1,
    sell: 0,
};


function prepare_transaction(transaction) {

    let url = transaction === transaction_types.buy?
        '/game/ajax/buy/':'/game/ajax/sell/';

    prepare_token();
    prepare_input_nicenumber();

    divs_hidden_by_default([
        $("#quantity-form"),
        $("#accept-form"),
        $("#trans-status"),
    ]);

    let asset = {
        name: '',
        type: '',
        quantity: 1
    };


    on_asset_transact(asset);


    $("#send-quantity").click(function () {
        //on quantity select
        asset.quantity = $("#quantity").val();
        show_information_form(asset, populate_accept_form, transaction)
    });

    $("#cancel-quantity").click(function () {
        //on cancel quantity form
        $("#quantity-form").hide(400);
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
        $("#trans-status").hide(400);
    });
}



