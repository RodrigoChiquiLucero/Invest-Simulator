$(document).ready(function () {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#quantity-form").hide(0);
    $("#accept-form").hide(0);
    $("#trans-status").hide(0);

    var asset_name = '';
    var quantity = 1;
    var asset_type = '';

    function populate_accept_form(div, data) {
        div.find("#name").html(data.name);
        div.find("#price").html(data.buy);
        div.find("#total").html(data.buy * quantity)
    }
    function populate_response_form(div, data) {
        let status = div.find("#status");
        let label = div.find("label");
        status.html(data.message);
        if(data.error) {
            label.html("We are very sorry but an error ocurred");
            status.css('color', 'red');
        } else {
            label.html("Transaction successfull!");
            status.css('color', 'green');
        }
        $("#loading").hide();
        $("#accept-t").show(500);
    }

    $(".action").click(function () {
        asset_name = $(this).attr("id");
        asset_type = $(this).attr("type");
        $("#quantity-form").show(500);
    });

    $("#send-q").click(function () {
        quantity = $("#quantity").val();

        $("#quantity-form").hide(400);
        $("#accept-form").show(500).stop(true)
            .delay(5000).hide(400);
        $.ajax({
            url: '/game/ajax/quote/' + asset_name,
            success: function (data) {
                populate_accept_form($("#accept-form"), data)
            },
            error: function (jqXHR, status, errorThrown) {
                $("#accept-form").find("label")
                    .html("This asset is not available anymore")
                    .css('color', 'red');
            }
        });
    });
    $("#cancel-q").click(function () {
        $("#quantity-form").hide(400);
    });

    $("#accept-p").click(function () {
        $("#accept-form").stop(true).hide(400);
        $("#trans-status").show(500).find("#accept-t").hide(0);

        $.ajax({
            url: '/game/ajax/buy/',
            type: 'post',
            data: {'name': asset_name,
                    'quantity': quantity,
                    'type': asset_type},
            success: function (data) {
                populate_response_form($("#trans-status"), data);
            },
            error: function (jqXHR, status, errorThrown) {
                populate_response_form($("#trans-status"), {
                    'error': true,
                    'message': status
                });
            }
        });
    });

    $("#cancel-p").click(function () {
        $("#accept-form").stop(true).hide(400);
        $("#quantity-form").show(500);
    });

    $("#accept-t").click(function () {
        $("#trans-status").hide(400);
    });


    $('input[type="number"]').niceNumber()
        .on("keypress", function (e) {
            switch (e.key) {
                case "1":
                case "2":
                case "3":
                case "4":
                case "5":
                case "6":
                case "7":
                case "8":
                case "9":
                case "0":
                case "Backspace":
                    return true;

                default:
                    return false;
            }
        });


});



