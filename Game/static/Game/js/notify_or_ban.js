var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//CONFIGURE TOASTS
toastr.options = {
    "closeButton": false,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "preventDuplicates": true,
    "onclick": notification_info,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "9000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut",
    "positionClass": "toast-top-center",
};

let notif_message_large = '';

function notification_info() {
    notify(notif_message_large)
}

function notify(msg) {
    toastr.clear();
    let notify = toastr.warning(msg);

    let $notifyContainer = jQuery(notify).closest('.toast-top-center');
    if ($notifyContainer) {
        $notifyContainer.css("margin-top", 100);
        $notifyContainer.css("color", "red");
    }
}


function notify_or_ban() {
    $.ajax({
        url: '/game/notify/or/ban',
        method: 'POST',
        success: function (data) {
            console.log(data);
            if (data['must_notifiy']) {
                notif_message_large = data['message_large'];
                notify(data['message_short']);
            }
        },
        error: function (jqXHR, status, errorThrown) {
            console.log(errorThrown)
        }
    })
}

notify_or_ban();
setInterval(notify_or_ban, 10000);
