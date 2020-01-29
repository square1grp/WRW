var getTrHTML = function (symptomID, symptomName, symptomLevels) {
    template = `
        <tr>
            <td class="align-middle" width="22%">
                <h4 class="mb-0">SymptomName</h4>
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
                <button id="remove-SymptomID" type="button" class="close" data-symptom-id="SymptomID">
                    <span aria-hidden="true">&times;</span>
                </button>
            </td>
        </tr>
    `;

    return template.replace(/SymptomName/gi, symptomName).replace(/SymptomID/gi, symptomID);
};

$(document).ready(function () {
    $("button.close:not(#add-symptom)").click(function () {
        var symptom_id = $(this).data("symptom-id");
        $(this).parents("tr").remove()

        $("select.symptoms option[value=" + symptom_id + "]").prop("disabled", false);
    });

    $("button#add-symptom").click(function () {
        var symptom_id = $("select.symptoms").val();

        if (symptom_id) {
            $.each(org_symptoms, function (idx, symptom) {
                if (symptom['id'] == symptom_id) {
                    var template = getTrHTML(symptom['id'], symptom['name'], symptom['levels']);

                    $("table.cus-list tbody").append(template);

                    $("button#remove-" + symptom['id']).click(function () {
                        $(this).parents("tr").remove()

                        $("select.symptoms option[value=" + symptom['id'] + "]").prop("disabled", false);
                    });

                    $("select.symptoms option[value=" + symptom['id'] + "]").prop("disabled", true);
                    $("select.symptoms").val("-1");
                }
            });
        }
    });
});