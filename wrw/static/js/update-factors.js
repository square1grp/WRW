var getTrHTML = function (factorID, factorTitle, factorLevels, is_daily_factor) {
    template = `
        <tr>
            <td class="align-middle" width="200px">
                <h5 class="mb-0">FactorTitle</h5>
                <input type="hidden" name="factor_`+ (is_daily_factor ? "Daily" : "Intermittent") + `_IDs" value="FactorID"/>
            </td>

            <td class="align-middle" width="500px">
                <div class="row mx-auto">
    `;

    for (i = 0; i < factorLevels.length - (is_daily_factor ? 0 : 1); i++) {
        template += `
            <div class="col text-center">
                <label for="radio_FactorID_`+ (i + 1) + `" class="text-center w-100">` + factorLevels[i] + `</label>
                <input id="radio_FactorID_`+ (i + 1) + `" type="radio" name="factor_FactorID_level" value="` + (i + 1) + `"/>
            </div>
        `;
    }

    template += `
                </div>
            </td>

            <td class="align-middle" width="200px">
                <input name="factor_FactorID_description" class="form-control" placeholder="Description">
            </td>

            <td class="align-middle">
                <div class="row mx-auto">
                    <button id="convert-factor-FactorID" class="btn btn-primary mr-2">Make ` + (is_daily_factor ? `Intermittent` : "Daily") + `</button>`;

    template += `
                    <button class="btn btn-danger delete" id="delete-factor-FactorID" type="button" data-factor-id="FactorID">
                        <i class="fa fa-times" aria-hidden="true"></i>
                    </button>
                </div>
            </td>
        </tr>
    `;

    return template.replace(/FactorTitle/gi, factorTitle).replace(/FactorID/gi, factorID);
};

$(document).ready(function () {
    var showAlert = function (msg) {
        $(".alert strong").text(msg);
        $(".alert").addClass("show");

        setTimeout(function () {
            $(".alert").removeClass("show");
        }, 500);

    };

    var addFactor = function (factor_id, is_daily_factor) {
        if (factor_id) {
            $.each(org_factors, function (idx, factor) {
                if (factor["id"] == factor_id) {
                    var template = getTrHTML(factor["id"], factor["title"], factor["levels"], is_daily_factor);

                    if (is_daily_factor) {
                        $("form.uf-form table.cdf-list tbody").append(template);
                    } else {
                        $("form.uf-form table.cif-list tbody").append(template);
                    }

                    $("form.uf-form tbody tr input[type=radio], form.uf-form tbody tr input[type=checkbox]").unbind().change(function () {
                        showAlert("Data Modified");
                    });

                    $("form.uf-form select.factors option[value=" + factor["id"] + "]").remove();
                    $("form.uf-form select.factors").val("-1");

                    $("form.uf-form button#convert-factor-" + factor["id"]).click(function () {
                        $(this).parents("tr").remove()

                        if (is_daily_factor)
                            convertToIntermittentFactor(factor["id"]);
                        else
                            convertToDailyFactor(factor["id"]);
                    });

                    $("form.uf-form button#delete-factor-" + factor["id"]).click(function () {
                        $(this).parents("tr").remove();

                        $("form.uf-form select.factors").append("<option value=" + factor["id"] + ">" + factor["title"] + "</option>");
                    });
                }
            });
        }
    };

    var convertToIntermittentFactor = function (factor_id) {
        addFactor(factor_id, false);
    };

    var convertToDailyFactor = function (factor_id) {
        addFactor(factor_id, true);
    };

    $("form.uf-form button.convert-to-daily").click(function () {
        $(this).parents("tr").remove()

        var factor_id = $(this).data("factor-id");
        convertToDailyFactor(factor_id);
    });

    $("form.uf-form button.convert-to-intermittent").click(function () {
        $(this).parents("tr").remove()

        var factor_id = $(this).data("factor-id");
        convertToIntermittentFactor(factor_id);
    });

    $("form.uf-form button.delete:not(.end-daily-factor)").click(function () {
        var factor_id = $(this).data("factor-id");
        $(this).parents("tr").remove()
        $.each(org_factors, function (idx, factor) {
            if (factor["id"] == factor_id) {
                $("form.uf-form select.factors").append("<option value=" + factor["id"] + ">" + factor["title"] + "</option>");
            }
        });
    });

    $("form.uf-form button#add-intermittent-factor").click(function () {
        var factor_id = $("select#a-intermittent-factors").val();

        if (factor_id) {
            if ($(this).hasClass("cif")) {

                if (factor_id > 0) {
                    window.location.href = "/user/" + user_id + "/update_factors/?action=add_cif&factor_id=" + factor_id;
                }
            } else {
                addFactor(factor_id, false)
            }
        }
    });

    $("form.uf-form button#add-daily-factor").click(function () {
        var factor_id = $("select#a-daily-factors").val();

        if (factor_id) {
            if ($(this).hasClass("udfs")) {
                var date = $("#date").val();
                var time = $("#time").val();

                if (factor_id > 0) {
                    window.location.href = "/user/" + user_id + "/update_factors/?action=add_udfs&factor_id=" + factor_id + "&date=" + date + "&time=" + time;
                }
            } else {
                addFactor(factor_id, true)
            }
        }
    });

    $("form.uf-form button.end-daily-factor").click(function () {
        var udfs_id = $(this).data("udfs-id");

        if (udfs_id && $(this).hasClass("udfe")) {
            var date = $("#date").val();
            var time = $("#time").val();

            if (udfs_id > 0) {
                window.location.href = "/user/" + user_id + "/update_factors/?action=add_udfe&udfs_id=" + udfs_id + "&date=" + date + "&time=" + time;
            }
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
});