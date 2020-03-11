$(document).ready(function () {
    var showAlert = function (msg) {
        $(".alert strong").text(msg);
        $(".alert").addClass("show");

        setTimeout(function () {
            $(".alert").removeClass("show");
        }, 500);

    };

    $("form.uf-form button.delete:not(.end-daily-factor)").click(function () {
        var factor_id = $(this).data("factor-id");
        $(this).parents("tr").remove()
        $.each(org_factors, function (idx, factor) {
            if (factor["id"] == factor_id) {
                $("form.uf-form select.factors").append("<option value=" + factor["id"] + ">" + factor["title"] + "</option>");
            }
        });
    });

    $("form.uf-form .cif.delete").click(function (e) {
        e.preventDefault();

        var factor_id = $(this).data("factor-id");
        $(this).parents("tr").remove()

        var delete_url = $(this).attr("href");
        $.post(delete_url, {
            action: "delete_cif",
            factor_id: factor_id
        }, function (res_data) {
            // console.log(res_data)
        });

        $.each(org_factors, function (idx, factor) {
            if (factor["id"] == factor_id) {
                $("form.uf-form select.factors").append("<option value=" + factor["id"] + ">" + factor["title"] + "</option>");
            }
        });
    });

    $("form.uf-form button#add-intermittent-factor").click(function () {
        var factor_id = $("select#a-intermittent-factors").val();

        if (factor_id > 0) {
            window.location.href = "/user/" + user_id + "/update_factors/?action=add_cif&factor_id=" + factor_id;
        }
    });

    $("form.uf-form button#add-daily-factor").click(function () {
        var factor_id = $("select#a-daily-factors").val();

        if (factor_id > 0) {
            var date = $("#date").val();
            var time = $("#time").val();

            window.location.href = "/user/" + user_id + "/update_factors/?action=add_udfs&factor_id=" + factor_id + "&date=" + date + "&time=" + time;
        }
    });

    $("form.uf-form button.end-daily-factor:not(:disabled)").click(function () {
        var udfs_id = $(this).data("udfs-id");

        if (udfs_id > 0) {
            var date = $("#date").val();
            var time = $("#time").val();

            window.location.href = "/user/" + user_id + "/update_factors/?action=add_udfe&udfs_id=" + udfs_id + "&date=" + date + "&time=" + time;
        }
    });

    $("#date_filter").change(function () {
        $("form.date_filter").submit();
    });

    $("form.uf-form tbody tr input[type=radio], form.uf-form tbody tr input[type=checkbox]").change(function () {
        showAlert("Data Modified");
    });

    $("form.uf-form").submit(function (e) {
        if (!$("form.uf-form .form-control:invalid").length) {
            e.preventDefault();

            showAlert("Data Updated");

            setTimeout(function () {
                $("form.uf-form").unbind().submit();
            }, 500);
        }
    });

    $("#date").change(function () {
        var date = $("#date").val();
        var time = $("#time").val();

        if (date && time) {
            window.location.href = "/user/" + user_id + "/update_factors/?date=" + date + "&time=" + time;
        }
    });

    $(".convert-to-intermittent:not(:disabled)").click(function () {
        var udfs_id = $(this).data("udfs-id");

        if (udfs_id > 0) {
            var date = $("#date").val();
            var time = $("#time").val();

            window.location.href = "/user/" + user_id + "/update_factors/?action=convert-to-intermittent&udfs_id=" + udfs_id + "&date=" + date + "&time=" + time;
        }
    });

    $(".convert-to-daily:not(:disabled)").click(function () {
        var factor_id = $(this).data("factor-id");

        if (factor_id > 0) {
            var date = $("#date").val();
            var time = $("#time").val();

            window.location.href = "/user/" + user_id + "/update_factors/?action=convert-to-daily&factor_id=" + factor_id + "&date=" + date + "&time=" + time;
        }
    });
});