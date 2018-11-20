window.onload = function () {

    prepare_token();

    let id = 'None';

    divs_hidden_by_default([
        $("#confirm-deletion-form"),
        $("#deletion-status"),
        $("#quantity-form"),
        $("#modification-status")
    ]);

    $(".offered_loans-deleter").click(function () {
        id = $(this).attr('id');
        $("#confirm-deletion-form").show(500);
        let delstatus = $("#deletion-status");
        delstatus.find('label').html(
            'Offered loan is being deleted'
        );
        delstatus.find('#cancel-deletion-onloading').val('CANCEL');
        delstatus.find('#loading').show();
    });

    $(".offered_loans-modifier").click(function () {
        id = $(this).attr('id');
        $("#quantity-form").show(500);
    });

    $("#send-confirm-deletion").click(function () {
        $("#confirm-deletion-form").hide(400);

        $("#deletion-status").show(500);

        let delete_timeout = setTimeout(
            function () {
                $.ajax({
                    url: '',
                    type: 'POST',
                    data: {
                        'id': id,
                        'method': 'delete'
                    },
                    success: function (data) {
                        populate_response(data['error'], data['message'], $('#deletion-status'));
                    },
                    error: function (jqXHR, status, errorThrown) {
                        populate_response(true, errorThrown, $('#deletion-status'));
                    }
                })
            }, 3000
        );

        $("#cancel-deletion").click(function () {
            clearTimeout(delete_timeout);
            $("#deletion-status").hide(500);
        });

    });

    $("#send-quantity").click(function () {
        $("#quantity-form").hide(400);

        $("#modification-status").show(500);

        let modify_loaned_money = setTimeout(
            function () {
                $.ajax({
                    url: '',
                    type: 'POST',
                    data: {
                        'id': id,
                        'new_offer': $('#quantity').val(),
                        'method': 'modify'
                    },
                    success: function (data) {
                        populate_response(data['error'], data['message'], $('#modification-status'));
                    },
                    error: function (jqXHR, status, errorThrown) {
                        populate_response(true, errorThrown, $('#modification-status'));
                    }
                })
            }, 3000
        );

        $("#cancel-modification").click(function () {
            clearTimeout(modify_loaned_money);
            $("#modification-status").hide(500);
        });

    });

    $("#cancel-quantity").click(function () {
        $("#quantity-form").hide(400);
    });

    $("#send-cancel-deletion").click(function () {
        $("#confirm-deletion-form").hide(400);
    });

    function populate_response(error, message, div) {
        div.find('#loading').hide();
        let label = div.find('label');
        label.css('font-weight', '2px');
        if (error) {
            label.css('color', 'red')
        } else {
            label.css('color', 'green')
        }
        label.html(message);
        div.find('.cancel').click(function () {
            div.hide(400);
            location.href = '';
        }).val('OK');
    }

};