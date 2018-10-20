$(document).ready(function () {
    var asset_name = '';
    var quantity = 1;

    function populate_accept_form(div, data) {
        div.find("#name").html(data.name);
        div.find("#price").html(data.buy);
        div.find("#total").html(data.buy * quantity)
    }

    $("#quantity-form").hide(0);
    $("#accept-form").hide(0);

    $(".action").click(function () {
        asset_name = $(this).attr("id");
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
        //    todo: pedir el precio de la accion segun la cantidad
        //    y mostrar la ventana de 5 seg
    });

    $("#cancel-p").click(function () {
        $("#accept-form").stop(true).hide(400);
        $("#quantity-form").show(500);
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



