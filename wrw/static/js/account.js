var hasWhiteSpace = function (s) {
    return s.indexOf(' ') >= 0;
};

$(document).ready(function () {
    $("#new_password, #confirm_password").change(function () {
        if (hasWhiteSpace($(this).val())) {
            this.setCustomValidity("invalid");
            return;
        } else {
            this.setCustomValidity("");
        }

        if ($("#new_password").val() != $("#confirm_password").val()) {
            $.each($("#new_password, #confirm_password"), function () {
                this.setCustomValidity("invalid");
            });
        } else {
            $.each($("#new_password, #confirm_password"), function () {
                this.setCustomValidity("");
            });
        }
    });

    $("#change-password-form").submit(function () {
        if ($("#change-password-form input:invalid").length > 0)
            return false;

        if ($("#new_password").val() != $("#confirm_password").val()) {
            $.each($("#new_password, #confirm_password"), function () {
                this.setCustomValidity("invalid");
            });
        } else {
            $.each($("#new_password, #confirm_password"), function () {
                this.setCustomValidity("");
            });
        }
    });
});