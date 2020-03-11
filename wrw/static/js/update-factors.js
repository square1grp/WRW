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
        $(this).parents("tr").remove();

        $.each(org_factors, function (idx, factor) {
            if (factor["id"] == factor_id) {
                $("form.uf-form select.factors").append("<option value=" + factor["id"] + ">" + factor["title"] + "</option>");
            }
        });
    });

    var bindEvents = function () {
        $("form.uf-form .cif.delete").bind("click", function (e) {
            e.preventDefault();

            var factor_id = $(this).data("factor-id");
            $(this).parents("tr").remove();

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
    };

    bindEvents();

    var unbindEvents = function () {
        $("form.uf-form .cif.delete").unbind("click");
    };

    $("form.uf-form button#add-intermittent-factor").click(function () {
        var factor_id = $("select#a-intermittent-factors").val();

        if (factor_id > 0) {
            $.each(org_factors, function (idx, factor) {
                if (factor["id"] == factor_id) {
                    $.post("/user/" + user_id + "/update_factors/", {
                        action: "add_cif",
                        factor_id: factor_id
                    }, function (res_data) {
                        if (res_data["added"]) {
                            var tr_template = `
                                <tr>
                                    <td class="align-middle" width="200px">
                                        <h5 class="mb-0">`+ factor["title"] + `</h5>
                                        <input type="hidden" name="factor_Intermittent_IDs" value="`+ factor["id"] + `"/>
                                    </td>

                                    <td class="align-middle" width="500px">
                                        <div class="row mx-auto">`;

                            $.each(factor["levels"], function (level_idx, level) {
                                if (level_idx > 4)
                                    return;

                                tr_template += `
                                            <div class="col px-1 text-center">
                                                <label for="radio_`+ factor["id"] + `_` + (level_idx + 1) + `" class="text-center w-100">` + level + `</label>
                                                <input id="radio_`+ factor["id"] + `_` + (level_idx + 1) + `" type="radio" name="factor_` + factor["id"] + `_level" value="` + (level_idx + 1) + `"/>
                                            </div>
                                `;
                            });

                            tr_template += `
                                        </div>
                                    </td>

                                    <td class="align-middle" width="200px">
                                        <input name="factor_`+ factor["id"] + `_description" class="form-control" placeholder="Description">
                                    </td>

                                    <td class="align-middle">
                                        <div class="row mx-auto">
                                            <button class="btn btn-primary mr-2 convert-to-daily" data-factor-id="`+ factor["id"] + `">Make Daily</button>
                                            <a class="btn btn-danger delete cif d-flex align-items-center" href="/user/`+ user_id + `/update_factors/" data-factor-id=` + factor["id"] + `>
                                                <i class="fa fa-times" aria-hidden="true"></i>
                                            </a>
                                        </div>
                                    </td>
                                </tr>
                            `;

                            $("table.cif-list tbody").append(tr_template);

                            if (factor["id"] == factor_id) {
                                $("form.uf-form select.factors option[value=" + factor["id"] + "]").remove();
                            }

                            unbindEvents();
                            bindEvents();
                        }
                    });
                }
            });
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
            $(this).parents("tr").remove();
            var date = $("#date").val();
            var time = $("#time").val();

            $.post("/user/" + user_id + "/update_factors/", {
                action: "add_udfe",
                udfs_id: udfs_id,
                date: date,
                time: time
            }, function (res_data) {
                // console.log(res_data)
            });
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