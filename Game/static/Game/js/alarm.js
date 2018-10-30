
window.onload = function () {
    prepare_token();

    $("#accept-success").click(
        function () {
            $("#trans-status").hide(500);
            $("#quantity-form").show(500);
        }
    );

    function populate_success(data) {
        $("#accept-success").show(500);
        $("#loading").hide(500);
        $("#trans-status").find('label').html(
            'Your alert has been set successfully!'
        );

    }

    function populate_error(error) {
        $("#accept-success").show(500);
        $("#loading").hide(500);
        $("#trans-status").find('label').html(
            error
        );
    }

    $("#general").click(function () {
        $(".selected-check").each(
            function () {
                $(this).attr('checked', $("#general").is(':checked'))
            }
        );
    });

    $("#trans-status").hide();

    $("#send-alert").click(function () {
        //take all selected assets
        let selected = [];
        $(".selected-check").each( function () {
                if($(this).is(':checked'))
                    selected.push($(this).attr('id'))
        });

        //what is the selected type?
        let isUp = $('input:radio[name=type]:checked').val();

        //what is the threshold?
        let threshold = $('#quantity').val();

        $("#quantity-form").hide(400);
        $("#trans-status").show(500).find("#accept-success").hide();
        $.ajax({
            url:'',
            type: 'post',
            data: {
                'isUp': isUp,
                'threshold': threshold,
                'assets': selected },
            success: function (data) {
                populate_success(data)
            },
            error: function (jqXHR, status, errorThrown) {
                populate_error(errorThrown)
            }

        });

    })
};
