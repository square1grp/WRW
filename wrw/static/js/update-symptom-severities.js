var getTrHTML = function (symptomID, symptomName, symptomLevels) {
    template = `
        <tr>
            <td class="align-middle" width="250px">
                <h5 class="mb-0">SymptomName</h5>
                <input type="hidden" name="symptom_IDs" value="SymptomID"/>
            </td>

            <td class="align-middle" width="550px">
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

            <td class="align-middle" width="250px">
                <input name="symptom_SymptomID_description" class="form-control" placeholder="Description">
            </td>

            <td class="align-middle">
                <div class="row mx-auto">
                    <button class="btn btn-danger delete" id="delete-symptom-SymptomID" type="button" data-symptom-id="SymptomID">
                        <i class="fa fa-times" aria-hidden="true"></i>
                    </button>
                </div>
            </td>
        </tr>
    `;

    return template.replace(/SymptomName/gi, symptomName).replace(/SymptomID/gi, symptomID);
};

$(document).ready(function () {
    var showAlert = function (msg) {
        $(".alert strong").text(msg);
        $(".alert").addClass("show");

        setTimeout(function () {
            $(".alert").removeClass("show");
        }, 500);

    };

    $("form.uss-form button.delete").click(function () {
        var symptom_id = $(this).data("symptom-id");
        $(this).parents("tr").remove()

        $.each(org_symptoms, function (idx, symptom) {
            if (symptom["id"] == symptom_id) {
                $("form.uss-form select.symptoms").append("<option value=" + symptom["id"] + ">" + symptom["name"] + "</option>");
            }
        });
    });

    $("form.uss-form button#add-symptom").click(function () {
        var symptom_id = $("select.symptoms").val();

        if (symptom_id) {
            $.each(org_symptoms, function (idx, symptom) {
                if (symptom["id"] == symptom_id) {
                    var template = getTrHTML(symptom["id"], symptom["name"], symptom["levels"]);

                    $("form.uss-form table.cus-list tbody").append(template);

                    $("form.uss-form button#delete-symptom-" + symptom["id"]).click(function () {
                        $(this).parents("tr").remove()

                        $("form.uss-form select.symptoms").append("<option value=" + symptom["id"] + ">" + symptom["name"] + "</option>");
                    });

                    $("form.uss-form tbody tr input[type=radio]").unbind().change(function () {
                        showAlert("Data Modified");
                    });

                    $("form.uss-form select.symptoms option[value=" + symptom["id"] + "]").remove()
                    $("form.uss-form select.symptoms").val("-1");
                }
            });
        }
    });

    $("#date_filter").change(function () {
        $("form.date_filter").submit();
    });

    $("form.uss-form tbody tr input[type=radio]").change(function () {
        showAlert("Data Modified");
    });

    $("form.uss-form").submit(function (e) {
        if (!$("form.uss-form .form-control:invalid").length) {
            e.preventDefault();

            showAlert("Data Updated");

            setTimeout(function () {
                $("form.uss-form").unbind().submit();
            }, 500);
        }
    });
});