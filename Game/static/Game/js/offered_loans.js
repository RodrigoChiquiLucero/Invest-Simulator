window.onload = function () {

    prepare_token();

    let loaned = 'None';
    let interest_rate = 'None';
    let days = 'None';
    let new_loan = 'None';


    divs_hidden_by_default([
        $("#confirm-deletion-form"),
        $("#deletion-status"),
        $("#quantity-form"),
        $("#modification-status")
    ]);

    $(".offered_loans-deleter").click(function () {
        loaned = $(this).attr('id');
        interest_rate = $(this).attr('interest_rate');
        days = $(this).attr('days');
        $("#confirm-deletion-form").show(500);
        let delstatus = $("#deletion-status");
        delstatus.find('label').html(
            'Offered loan is being deleted'
        );
        delstatus.find('#loading').show();
    });

    $(".offered_loans-modifier").click(function () {
        loaned = $(this).attr('id');
        new_loan = $("#quantity").val();
        interest_rate = $(this).attr('interest_rate');
        days = $(this).attr('days');
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
                        'loaned': loaned,
                        'interest_rate': interest_rate,
                        'days': days,
                        'method': 'delete'
                    },
                    success: function () {
                        $("#deletion-status").hide(500);
                        location.href = "";
                    },
                    error: function () {
                        let delstatus = $("#deletion-status");
                        delstatus.find('label').html(
                            'An error ocurred while deleting offered loan'
                        );
                        delstatus.find('#loading').hide();
                        delstatus.find('#cancel-deletion-onloading').val('OK');
                    }
                })
            }, 3000
        );

        $("#cancel-deletion-onloading").click(function () {
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
                        'loaned': loaned,
                        'interest_rate': interest_rate,
                        'days': days,
                        'new_loan': new_loan,
                        'method': 'modify'
                    },
                    success: function () {
                        $("#modification-status").show(500);
                        location.href = "";
                    },
                    error: function () {
                        let delstatus = $("#deletion-status");
                        delstatus.find('label').html(
                            'An error ocurred while modifying offered loan'
                        );
                        delstatus.find('#loading').hide();
                        delstatus.find('#cancel-deletion-onloading').val('OK');
                    }
                })
            }, 3000
        );

        $("#cancel-deletion-onloading").click(function () {
            clearTimeout(modify_loaned_money);
            $("#deletion-status").hide(500);
        });

    });

    $("#cancel-quantity").click(function () {
        $("#quantity-form").hide(400);
    });

    $("#send-cancel-deletion").click(function () {
        $("#confirm-deletion-form").hide(400);
    });

};