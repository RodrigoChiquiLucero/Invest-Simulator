window.onload = function () {
    //hide by default
    $('#alert-options').hide();

    $('#alert').click(function () {
        $('#all').hide(400);
        $('#alert-options').show(500);
    });

    $('#back').click(function () {
        $('#alert-options').hide(400);
        $('#all').show(500);
    });
};
