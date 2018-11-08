window.onload = function () {
    let loan = null;

    prepare_token();
    prepare_input_nicenumber();

    divs_hidden_by_default([
        $('#loan-liquid-form'),
        $('#accept-loan-form'),
        $('#result'),
    ]);

    $('.take').click(function () {
        loan = JSON.parse($(this).attr('id').replace(/'/g, '"'));
        $('#loan-offers').hide(400);
        $('#loan-liquid-form').show(500);
    });
    $('#cancel-quantity').click(function () {
        loan_id = null;
        $('#loan-offers').show(500);
        $('#loan-liquid-form').hide(400);
    });

    $('#send-quantity').click(function () {
        $('#loan-liquid-form').hide(400);
        let quantity = parseFloat($('#quantity').val());
        let loaned = parseFloat(loan.offered_with_loans);
        let interest = parseFloat(loan.interest_rate);

        console.log(loan);

        if (quantity > loaned){
            $('#result').show(500)
                .find('#loading').hide();
            return;
        }

        quantity = quantity
            + (quantity * interest/100);

        let someDate = new Date();
        let numberOfDaysToAdd = loan.days;
        someDate.setDate(someDate.getDate() + numberOfDaysToAdd);
        let dd = someDate.getDate();
        let mm = someDate.getMonth() + 1;
        let y = someDate.getFullYear();
        let someFormattedDate = dd + '/' + mm + '/' + y;
        $('#accept-loan-form').show(500).find('p').html(
            `If you press <b>accept</b> you will have to return
            $${quantity} by ${someFormattedDate}, if you fail to return it,
            you will be kicked out the game, and you will lose all your
            wallet purchases. There is no turning back.`
        );
    });

    $('#accept-result').click(function () {
        $('#result').hide(400);
        $('#loan-liquid-form').show(500);
    });

    $('#cancel-loan').click(function () {
        $('#accept-loan-form').hide(400);
        $('#loan-liquid-form').show(500);
    });


    $('#accept-loan').click(function () {
        console.log('Entramos');
        $('#accept-loan-form').hide(400);
        $('#result').show(500)
            .find('#loading').hide();
        $.ajax({
            url: '',
            type:'POST',
            data: {
                'id': loan.id,
                'loaned': parseFloat($('#quantity').val())},
            success: function (data) {
                $('#loading').hide();
                $('#result-content').html("Your loan has been taken successfully!");
                $('#accept-result').click(function () {
                    $('#result').hide(400);
                    $('#loan-offers').show(500);
                    location.href = "";
                });
            },
            error: function (jqXHR, status, errorThrown) {
                $('#loading').hide();
                $('#result-content').html(errorThrown);
            }
        });
    });

};