window.onload = function () {

    prepare_token();
    let id = 'None';
    let loan = 'None';

    prepare_input_nicenumber();

    divs_hidden_by_default([
        $("#quantity-form"),
        $("#confirm-deletion-form")
    ]);

    $(".modify").click(function () {
        id = $(this).attr('id');
        loan = $(this).attr('loan');
        $("#quantity-form").show(500);


    });
    $("#send-quantity").click(function () {
        let quantity = $("#quantity");
        $.ajax({
            url: 'loans/offered',
            type: 'POST',
            data: {
                'id': id,
                'loan': loan,
                'quantity': quantity,
            },
            success: function () {
                $("#quantity-form").hide(500);
                $("#confirm-deletion-form").show(500);
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
    });

    $("#cancel-quantity").click(function () {
        $("#quantity-form").hide(500);
    });
};
