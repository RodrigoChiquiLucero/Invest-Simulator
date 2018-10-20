$(document).ready(function () {
    $("#quantity-form").hide(0);

    $("#action").click(function () {
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

    $('input[type="number"]').niceNumber();

});



