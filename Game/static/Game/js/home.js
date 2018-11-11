window.onload = function () {
    //hide by default
    $('#alert-options').hide();
    $('#loan-options').hide();

    $('#alert').click(function () {
        $('#all').hide(400);
        $('#alert-options').show(500);
    });

    $('#loan').click(function () {
        $('#all').hide(400);
        $('#loan-options').show(500);
    });

    $('#alert_back').click(function () {
        $('#alert-options').hide(400);
        $('#all').show(500);
    });

    $('#loan_back').click(function () {
        $('#loan-options').hide(400);
        $('#all').show(500);
    });
};