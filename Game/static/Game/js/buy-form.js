$(document).ready(function () {
    var asset_name = '';

    $("#quantity-form").hide(0);

    $(".action").click(function () {
        asset_name = $(this).attr("id");
        console.log(asset_name);
        $("#quantity-form").show(500);
    });

    $("#send-q").click(function () {
        $("#quantity-form").hide(400);
        //    todo: pedir el precio de la accion segun la cantidad
        //    y mostrar la ventana de 5 seg
    });

    $("#cancel-q").click(function () {
        $("#quantity-form").hide(400);
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
        })
});



