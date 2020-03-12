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

            $.post("/user/" + user_id + "/update_factors/", {
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

        $("form.uf-form button.end-daily-factor:not(:disabled)").bind("click", function () {
            var udfs_id = $(this).data("udfs-id");
            var factor_id = $(this).data("factor-id");

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

                $.each(org_factors, function (idx, factor) {
                    if (factor["id"] == factor_id) {
                        $("form.uf-form select.factors").append("<option value=" + factor["id"] + ">" + factor["title"] + "</option>");
                    }
                });
            }
        });

        $(".convert-to-intermittent:not(:disabled)").bind("click", function () {
            var factor_id = $(this).siblings("button.delete").data("factor-id");
            $(this).siblings("button.delete").trigger("click");
            addIntermittentFactor(factor_id);
        });

        $(".convert-to-daily:not(:disabled)").bind("click", function () {
            var factor_id = $(this).siblings("button.delete").data("factor-id");
            $(this).siblings("button.delete").trigger("click");
            addDailyFactor(factor_id);
        });
    };

    bindEvents();

    var unbindEvents = function () {
        $("form.uf-form .cif.delete").unbind("click");
        $("form.uf-form button.end-daily-factor:not(:disabled)").unbind("click");
        $(".convert-to-intermittent:not(:disabled)").unbind("click");
        $(".convert-to-daily:not(:disabled)").unbind("click");
    };

    var addIntermittentFactor = function (factor_id) {
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
                                        <button class="btn btn-danger delete cif d-flex align-items-center" data-factor-id=` + factor["id"] + `>
                                            <i class="fa fa-times" aria-hidden="true"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        `;

                        $("table.cif-list tbody").append(tr_template);

                        $("form.uf-form select.factors option[value=" + factor["id"] + "]").remove();

                        unbindEvents();
                        bindEvents();
                    }
                });
            }
        });
    };

    var addDailyFactor = function (factor_id) {
        var date = $("#date").val();
        var time = $("#time").val();

        $.each(org_factors, function (idx, factor) {
            if (factor["id"] == factor_id) {
                $.post("/user/" + user_id + "/update_factors/", {
                    action: "add_udfs",
                    factor_id: factor_id,
                    date: date,
                    time: time
                }, function (res_data) {
                    if (res_data["added"]) {
                        var tr_template = `
                            <tr>
                                <td class="align-middle" width="200px">
                                    <h5 class="mb-0">`+ factor["title"] + `</h5>
                                    <input type="hidden" name="udfs_IDs" value="`+ res_data["udfs_id"] + `"/>
                                </td>

                                <td class="align-middle" width="500px">
                                    <div class="row mx-auto">`;

                        $.each(factor["levels"], function (level_idx, level) {
                            tr_template += `
                                        <div class="col px-1 text-center">
                                            <label for="radio_`+ res_data["udfs_id"] + `_` + (level_idx + 1) + `" class="text-center w-100">` + level + `</label>
                                            <input id="radio_`+ res_data["udfs_id"] + `_` + (level_idx + 1) + `" type="radio" name="udfs_` + res_data["udfs_id"] + `_level" value="` + (level_idx > 4 ? 0 : (level_idx + 1)) + `"/>
                                        </div>
                            `;
                        });

                        tr_template += `
                                    </div>
                                </td>

                                <td class="align-middle" width="200px">
                                    <input name="udfs_`+ res_data["udfs_id"] + `_description" class="form-control" placeholder="Description">
                                </td>

                                <td class="align-middle">
                                    <div class="row mx-auto">
                                        <button class="btn btn-primary mr-2 convert-to-intermittent" data-udfs-id="`+ res_data["udfs_id"] + `" data-factor-id="` + res_data["factor_id"] + `">Make Intermittent</button>

                                        <button class="btn btn-danger delete end-daily-factor" type="button" data-udfs-id="`+ res_data["udfs_id"] + `" data-factor-id="` + res_data["factor_id"] + `">
                                            <i class="fa fa-times" aria-hidden="true"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        `;

                        $("table.cdf-list tbody").append(tr_template);

                        $("form.uf-form select.factors option[value=" + factor["id"] + "]").remove();

                        unbindEvents();
                        bindEvents();
                    }
                });
            }
        });
    };

    $("form.uf-form button#add-intermittent-factor").click(function () {
        var factor_id = $("select#a-intermittent-factors").val();

        if (factor_id > 0) {
            addIntermittentFactor(factor_id);
        }
    });

    $("form.uf-form button#add-daily-factor").click(function () {
        var factor_id = $("select#a-daily-factors").val();

        if (factor_id > 0) {
            addDailyFactor(factor_id);
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
});