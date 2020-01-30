var getTrHTML = function (symptomID, symptomName, symptomLevels) {
    template = `
        <tr>
            <td class="align-middle" width="22%">
                <h5 class="mb-0">SymptomName</h5>
                <input type="hidden" name="symptom_IDs" value="SymptomID"/>
            </td>

            <td class="align-middle" width="58%">
                <div class="row mx-auto">
    `;

    for (i = 0; i < symptomLevels.length; i++) {
        template += `
            <div class="col text-center">
                <label for="radio_SymptomID_`+ (i + 1) + `" class="text-center w-100">` + symptomLevels[i] + `</label>
                <input id="radio_SymptomID_`+ (i + 1) + `" type="radio" name="symptom_SymptomID_level" value="` + (i + 1) + `"/>
            </div>
        `;
    }

    template += `
                </div>
            </td>

            <td class="align-middle" width="20%">
                <input name="symptom_SymptomID_description" class="form-control" placeholder="Description">
            </td>

            <td class="align-middle" width="10%">
                <button class="btn btn-danger delete" id="delete-symptom-SymptomID" type="button" data-symptom-id="SymptomID">
                    <i class="fa fa-times" aria-hidden="true"></i>
                </button>
            </td>
        </tr>
    `;

    return template.replace(/SymptomName/gi, symptomName).replace(/SymptomID/gi, symptomID);
};

$(document).ready(function () {
    $("form.uss-form button.delete").click(function () {
        var symptom_id = $(this).data("symptom-id");
        $(this).parents("tr").remove()

        $("form.uss-form select.symptoms option[value=" + symptom_id + "]").prop("disabled", false);
    });

    $("form.uss-form button#add-symptom").click(function () {
        var symptom_id = $("select.symptoms").val();

        if (symptom_id) {
            $.each(org_symptoms, function (idx, symptom) {
                if (symptom['id'] == symptom_id) {
                    var template = getTrHTML(symptom['id'], symptom['name'], symptom['levels']);

                    $("form.uss-form table.cus-list tbody").append(template);

                    $("form.uss-form button#delete-symptom-" + symptom['id']).click(function () {
                        $(this).parents("tr").remove()

                        $("form.uss-form select.symptoms option[value=" + symptom['id'] + "]").prop("disabled", false);
                    });

                    $("form.uss-form select.symptoms option[value=" + symptom['id'] + "]").prop("disabled", true);
                    $("form.uss-form select.symptoms").val("-1");
                }
            });
        }
    });

    $("#date_filter").change(function () {
        $("form.date_filter").submit();
    });
});