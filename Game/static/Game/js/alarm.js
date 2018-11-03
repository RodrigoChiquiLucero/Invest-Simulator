window.onload = function () {
    prepare_token();

    divs_hidden_by_default([
        $("#quantity-form"),
        $("#accept-form"),
        $("#trans-status"),
        $(".up-info"),
    ]);

    $(".set-alarm").click(
        function () {
            console.log("Entramos");
            $("#asset-table").hide(400);
            asset = $(this).attr("id");
            $("#quantity-form").show(500)
                .find("#qform-title")
                .html(
                    `Your alarm configuration for ${asset}`
                );
        }
    );

    $("#accept-success").click(
        function () {
            $("#trans-status").hide(500);
            $("#asset-table").show(500);
        }
    );

    function populate_success(data) {
        $("#accept-success").show(500);
        $("#loading").hide(500);
        $("#trans-status").find('#status-info').html(
            data.message
        );

    }

    function populate_error(error) {
        $("#accept-success").show(500);
        $("#loading").hide(500);
        $("#trans-status").find('#status-info').html(
            error
        );
    }

    $("#trans-status").hide();

    $("#send-alert").click(function () {
        //what is the selected type?
        let type = $('input:radio[name=type]:checked').val();
        console.log(type);

        //what is the threshold?
        let threshold = $('#quantity').val();

        $("#quantity-form").hide(400);
        $("#trans-status").show(500).find("#accept-success").hide();
        $.ajax({
            url: '',
            type: 'post',
            data: {
                'type': type,
                'asset_price' :'buy',
                'threshold': threshold,
                'asset': asset
            },
            success: function (data) {
                populate_success(data)
            },
            error: function (jqXHR, status, errorThrown) {
                populate_error(errorThrown)
            }

        });

    });

    $("#cancel-alert").click(
        function () {
            $("#quantity-form").hide(400);
            $("#asset-table").show(500);
        }
    );

    $("#choice1").click(
        function () {
            $(".up-info").show(400);
            $(".down-info").hide(400);
        }
    );

    $("#choice2").click(
        function () {
            $(".down-info").show(400);
            $(".up-info").hide(400);
        }
    ).click();

    /* --------------- RADIO ------------------*/

    const st = {};

    st.flap = document.querySelector('#flap');
    st.toggle = document.querySelector('.toggle');

    st.choice1 = document.querySelector('#choice1');
    st.choice2 = document.querySelector('#choice2');

    st.flap.addEventListener('transitionend', () => {

        if (st.choice1.checked) {
            st.toggle.style.transform = 'rotateY(-15deg)';
            setTimeout(() => st.toggle.style.transform = '', 400);
        } else {
            st.toggle.style.transform = 'rotateY(15deg)';
            setTimeout(() => st.toggle.style.transform = '', 400);
        }

    });

    st.clickHandler = (e) => {

        if (e.target.tagName === 'LABEL') {
            setTimeout(() => {
                st.flap.children[0].textContent = e.target.textContent;
            }, 250);

        }
    };

    document.addEventListener('DOMContentLoaded', () => {
        st.flap.children[0].textContent = st.choice2.nextElementSibling.textContent;
    });

    document.addEventListener('click', (e) => st.clickHandler(e));
};
