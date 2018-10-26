function readURL(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {
            $('#blah')
                .attr('src', e.target.result)
                .width(150)
                .height(150);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "preventDuplicates": true,
    "onclick": null,
    "showDuration": "100",
    "hideDuration": "100",
    "timeOut": "100000",
    "extendedTimeOut": "100",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut",
    "positionClass": "toast-bottom-center",
};


$(document).ready(
    function () {

        $(window).capslockstate();

        $(window).bind("capsChanged", function (event) {
            if ($(window).capslockstate("state") === true) {
                toastr.warning("Caps lock is on! Be careful!");
            } else {
                toastr.clear()
            }
        });

    }
)
;


