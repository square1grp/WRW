var getTrHTML = function (factorID, factorTitle, factorLevels, is_daily_factor) {
    template = `
        <tr>
            <td class="align-middle" width="15%">
                <h5 class="mb-0">FactorTitle</h5>
                <input type="hidden" name="factor_IDs" value="FactorID"/>
            </td>

            <td class="align-middle" width="50%">
                <div class="row mx-auto">
    `;

    for (i = 0; i < factorLevels.length; i++) {
        template += `
            <div class="col text-center">
                <label for="radio_FactorID_`+ (i + 1) + `" class="text-center w-100">` + factorLevels[i] + `</label>
                <input id="radio_FactorID_`+ (i + 1) + `" type="radio" name="symptom_FactorID_level" value="` + (i + 1) + `"/>
            </div>
        `;
    }

    if (is_daily_factor) {
        template += `
            <div class="col text-center">
                <label for="radio_{{cdf.factor.id}}_skipped" class="text-center w-100">Skipped?</label>
                <input id="radio_{{cdf.factor.id}}_skipped" type="checkbox" name="factor_{{cdf.factor.id}}_skipped" value="yes"/>
            </div>
        `;
    }

    template += `
                </div>
            </td>

            <td class="align-middle" width="20%">
                <input name="symptom_FactorID_description" class="form-control" placeholder="Description">
            </td>

            <td class="align-middle" width="10%">
                <button class="btn btn-danger delete" id="delete-factor-FactorID" type="button" data-symptom-id="FactorID">
                    <i class="fa fa-times" aria-hidden="true"></i>
                </button>
            </td>
        </tr>
    `;

    return template.replace(/FactorTitle/gi, factorTitle).replace(/FactorID/gi, factorID);
};

$(document).ready(function () {
    var addFactor = function (is_daily_factor) {
        var factor_id = $("select.factors").val();

        if (factor_id) {
            $.each(org_factors, function (idx, factor) {
                if (factor['id'] == factor_id) {
                    var template = getTrHTML(factor['id'], factor['title'], factor['levels'], is_daily_factor);

                    if (is_daily_factor)
                        $("form.ufs-form table.cdf-list tbody").append(template);
                    else
                        $("form.ufs-form table.cif-list tbody").append(template);

                    $("form.ufs-form button#delete-factor-" + factor['id']).click(function () {
                        $(this).parents("tr").remove()

                        $("form.ufs-form select.factors option[value=" + factor['id'] + "]").prop("disabled", false);
                    });

                    $("form.ufs-form select.factors option[value=" + factor['id'] + "]").prop("disabled", true);
                    $("form.ufs-form select.factors").val("-1");
                }
            });
        }
    };

    $("form.ufs-form button.delete").click(function () {
        var factor_id = $(this).data("factor-id");
        $(this).parents("tr").remove()

        $("form.ufs-form select.factors option[value=" + factor_id + "]").prop("disabled", false);
    });

    $("form.ufs-form button#add-intermittent-factor").click(function () {
        addFactor(false)
    });

    $("form.ufs-form button#add-daily-factor").click(function () {
        addFactor(true);
    });
});