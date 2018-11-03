window.onload = function () {

    prepare_token();

    let asset = 'None';
    let type = 'None';
    let price = 'None';

    divs_hidden_by_default([
        $("#confirm-deletion-form"),
        $("#deletion-status"),
    ]);

    $(".alarm-deleter").click(function () {
        asset = $(this).attr('id');
        type = $(this).attr('type');
        price = $(this).attr('price');
        $("#confirm-deletion-form").show(500);
        let delstatus = $("#deletion-status");
        delstatus.find('label').html(
            'Alert is being deleted'
        );
        delstatus.find('#loading').show();
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
                        'name': asset,
                        'type': type,
                        'price': price,
                        'method': 'delete'},
                    success: function () {
                        $("#deletion-status").hide(500);
                        location.href = "";
                    },
                    error: function () {
                        let delstatus = $("#deletion-status");
                        delstatus.find('label').html(
                            'An error ocurred while deleting alert'
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

    $("#send-cancel-deletion").click(function () {
        $("#confirm-deletion-form").hide(400);
    });

};