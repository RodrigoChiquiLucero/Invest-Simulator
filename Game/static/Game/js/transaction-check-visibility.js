window.onload = function () {

    prepare_token();

    divs_hidden_by_default([
        $("#visibility-change"),
        $("#change-status"),
        $("#cancel-deletion")
    ]);

    $(".visibility-modifier").click(function () {
        id = $(this).attr('id');
        $("#visibility-change").show(500);
    });

    $("#send-cancel-change").click(function () {
        $("#visibility-change").hide(400);
    });

    $("#send-confirm-change").click(function () {
        $("#visibility-change").hide(400);

        $("#change-status").show(500);

        let delete_timeout = setTimeout(
            function () {
                $.ajax({
                    url: '',
                    type: 'POST',
                    data: {
                        'id': id,
                        'method': 'change'
                    },
                    success: function (data) {
                        populate_response(data['error'], data['message'], $('#change-status'));
                    },
                    error: function (jqXHR, status, errorThrown) {
                        populate_response(true, errorThrown, $('#change-status'));
                    }
                })
            }, 3000
        );

        $("#cancel-deletion").click(function () {
            clearTimeout(delete_timeout);
            $("#change-status").hide(500);
        });

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


