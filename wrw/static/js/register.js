var hasWhiteSpace = function (s) {
    return s.indexOf(' ') >= 0;
};

$(document).ready(function () {
    $("#first_name").change(function () {
        var first_name = $("#first_name").val();
        $("#first_name").val(first_name.charAt(0).toUpperCase() + first_name.slice(1));
    });

    $("#last_name").change(function () {
        var last_name = $("#last_name").val();
        $("#last_name").val(last_name.charAt(0).toUpperCase() + last_name.slice(1));
    });

    $("#username").change(function () {
        if (hasWhiteSpace($(this).val())) {
            this.setCustomValidity("invalid");
        } else {
            this.setCustomValidity("");
        }
    });

    $("#password, #confirm_password").change(function () {
        if (hasWhiteSpace($(this).val())) {
            this.setCustomValidity("invalid");
            return;
        } else {
            this.setCustomValidity("");
        }


        if ($("#password").val() != $("#confirm_password").val()) {
            $.each($("#password, #confirm_password"), function () {
                this.setCustomValidity("invalid");
            });
        } else {
            $.each($("#password, #confirm_password"), function () {
                this.setCustomValidity("");
            });
        }
    });

    $("#register-form").submit(function () {
        $.each($("#password, #confirm_password"), function () {
            if (hasWhiteSpace($(this).val())) {
                this.setCustomValidity("invalid");
                return;
            } else {
                this.setCustomValidity("");
            }
        });

        if ($("#password").val() != $("#confirm_password").val()) {
            $.each($("#password, #confirm_password"), function () {
                this.setCustomValidity("invalid");
            });
        } else {
            $.each($("#password, #confirm_password"), function () {
                this.setCustomValidity("");
            });
        }
    });
});


$(function () {
    window.verifyRecaptchaCallback = function (response) {
        $('input[data-recaptcha]').val(response).trigger('change');
    }

    window.expiredRecaptchaCallback = function () {
        $('input[data-recaptcha]').val("").trigger('change');
    }

    $('#register-form').validator();
});