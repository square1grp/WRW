$(document).ready(function () {
    var showAlert = function (msg) {
        $(".alert strong").text(msg);
        $(".alert").addClass("show");

        setTimeout(function () {
            $(".alert").removeClass("show");
        }, 500);
    };

    var refreshFactorDropdowns = function () {
        $("form.uf-form select.factors option").remove();

        $("form.uf-form select.factors").append("<option value=-1>Please select factor</option>");

        $.each(org_factors, function (factor_idx, factor) {
            $("form.uf-form select.factors").append("<option value=" + factor["id"] + ">" + factor["title"] + "</option>");
        });

        $.each($("table.cif-list tbody tr button.delete, table.cdf-list tbody tr button.delete"), function (btn_idx, btn_selector) {
            var factor_id = $(btn_selector).data("factor-id");

            if ($("form.uf-form select.factors option[value=" + factor_id + "]").length)
                $("form.uf-form select.factors option[value=" + factor_id + "]").remove();
        });
    };

    $("form.uf-form button.delete:not(.end-daily-factor)").click(function () {
        var factor_id = $(this).data("factor-id");
        $(this).parents("tr").remove();

        refreshFactorDropdowns();
    });

    var bindEvents = function () {
        $("form.uf-form .cif.delete").bind("click", function (e) {
            e.preventDefault();

            var factor_id = $(this).data("factor-id");
            $(this).parents("tr").remove();

            $.post(ajax_url, {
                action: "delete_cif",
                factor_id: factor_id
            }, function (res_data) {
                // console.log(res_data)
            });

            refreshFactorDropdowns();
        });

        $("form.uf-form button.end-daily-factor:not(:disabled)").bind("click", function () {
            var udfs_id = $(this).data("udfs-id");
            var factor_id = $(this).data("factor-id");

            if (udfs_id > 0) {
                $(this).parents("tr").remove();
                var date = $("#date").val();
                var time = $("#time").val();

                $.post(ajax_url, {
                    action: "add_udfe",
                    udfs_id: udfs_id,
                    date: date,
                    time: time
                }, function (res_data) {
                    // console.log(res_data)
                });

                refreshFactorDropdowns();
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

    var resetEvents = function () {
        unbindEvents();
        bindEvents();
    };

    var getIntermittentFactorRowTemplate = function (factor) {
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

        return tr_template;
    };

    var getDailyFactorRowTemplate = function (udfs) {
        var tr_template = `
            <tr>
                <td class="align-middle" width="200px">
                    <h5 class="mb-0">`+ udfs.factor.title + `</h5>
                    <input type="hidden" name="udfs_IDs" value="`+ udfs.id + `"/>
                </td>

                <td class="align-middle" width="500px">
                    <div class="row mx-auto">`;

        $.each(udfs.factor.levels, function (level_idx, level) {
            tr_template += `
                        <div class="col px-1 text-center">
                            <label for="radio_`+ udfs.id + `_` + (level_idx + 1) + `" class="text-center w-100">` + level + `</label>
                            <input id="radio_`+ udfs.id + `_` + (level_idx + 1) + `" type="radio" name="udfs_` + udfs.id + `_level" value="` + (level_idx > 4 ? 0 : (level_idx + 1)) + `"/>
                        </div>
            `;
        });

        tr_template += `
                    </div>
                </td>

                <td class="align-middle" width="200px">
                    <input name="udfs_`+ udfs.id + `_description" class="form-control" placeholder="Description">
                </td>

                <td class="align-middle">
                    <div class="row mx-auto">
                        <button class="btn btn-primary mr-2 convert-to-intermittent" data-udfs-id="`+ udfs.id + `" data-factor-id="` + udfs.factor.id + `" ` + (udfs.disabled ? `disabled` : ``) + `>Make Intermittent</button>

                        <button class="btn btn-danger delete end-daily-factor" type="button" data-udfs-id="`+ udfs.id + `" data-factor-id="` + udfs.factor.id + `" ` + (udfs.disabled ? `disabled` : ``) + `>
                            <i class="fa fa-times" aria-hidden="true"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;

        return tr_template;
    };

    var addIntermittentFactor = function (factor_id) {
        $.each(org_factors, function (idx, factor) {
            if (factor["id"] == factor_id) {
                $.post(ajax_url, {
                    action: "add_cif",
                    factor_id: factor_id
                }, function (res_data) {
                    if (res_data.added) {
                        $("table.cif-list tbody").append(getIntermittentFactorRowTemplate(factor));

                        resetEvents();
                    }
                });
            }
        });

        refreshFactorDropdowns();
    };

    var addDailyFactor = function (factor_id) {
        var date = $("#date").val();
        var time = $("#time").val();

        $.each(org_factors, function (idx, factor) {
            if (factor["id"] == factor_id) {
                $.post(ajax_url, {
                    action: "add_udfs",
                    factor_id: factor_id,
                    date: date,
                    time: time
                }, function (res_data) {
                    $("table.cdf-list tbody tr").remove();

                    $.each(res_data.udfs_list, function (udfs_idx, udfs) {
                        $("table.cdf-list tbody").append(getDailyFactorRowTemplate(udfs));
                    });

                    refreshFactorDropdowns();

                    resetEvents();
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
        var date_filter = $("#date_filter").val();

        $.post(ajax_url, {
            action: "get_uf_list",
            date_filter: date_filter
        }, function (res_data) {
            $("table.uf-list tbody tr").remove();

            $.each(res_data.uf_list, function (uf_idx, uf) {
                var tr_template = `
                    <tr>
                        <td class="align-middle"><h5 class="mb-0">`+ uf.title + `</h5></td>
                        <td class="align-middle"><h5 class="mb-0">`+ uf.date + `</h5></td>
                        <td class="align-middle"><h5 class="mb-0">`+ uf.time + `</h5></td>
                        <td class="align-middle">
                            <div class="row mx-auto">
                                <form class="my-auto ml-auto mr-2" method="POST">
                                    <input type="hidden" name="action" value="edit_uf"/>
                                    <input type="hidden" name="uf_id" value="`+ uf.id + `"/>
                                    <input type="hidden" name="date_filter" value="`+ date_filter + `"/>

                                    <button class="btn btn-success edit" type="submit">
                                        <i class="fa fa-pencil" aria-hidden="true"></i>
                                    </button>
                                </form>

                                <form class="my-auto" method="POST">
                                    <input type="hidden" name="action" value="delete"/>
                                    <input type="hidden" name="uf_id" value="`+ uf.id + `"/>

                                    <button class="btn btn-danger delete" type="submit">
                                        <i class="fa fa-times" aria-hidden="true"></i>
                                    </button>
                                </form>
                            </div>
                        </td>
                    </tr>
                `;

                $("table.uf-list tbody").append(tr_template);
            });
        });
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
            $.post(ajax_url, {
                action: "get_daily_factors",
                date: date,
                time: time
            }, function (res_data) {
                $("#title").val(res_data.current_title);
                $("#date").datepicker("setDate", res_data.current_date);
                $("#time").val(res_data.current_time);

                $("table.cdf-list tbody tr").remove();

                $.each(res_data.udfs_list, function (udfs_idx, udfs) {
                    $("table.cdf-list tbody").append(getDailyFactorRowTemplate(udfs));
                });

                refreshFactorDropdowns();

                resetEvents();
            });
        }
    });
});