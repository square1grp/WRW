$(document).ready(function () {
    var showAlert = function (msg) {
        $(".alert strong").text(msg);
        $(".alert").addClass("show");

        setTimeout(function () {
            $(".alert").removeClass("show");
        }, 500);

    };

    var bindEvents = function () {
        $("form.uss-form .cus.delete").bind("click", function (e) {
            e.preventDefault();

            var symptom_id = $(this).data("symptom-id");
            $(this).parents("tr").remove()

            var delete_url = $(this).attr("href");
            $.post(delete_url, {
                action: "delete_cus",
                symptom_id: symptom_id
            }, function (res_data) {
                // console.log(res_data)
            });

            $.each(org_symptoms, function (idx, symptom) {
                if (symptom["id"] == symptom_id) {
                    $("form.uss-form select.symptoms").append("<option value=" + symptom["id"] + ">" + symptom["name"] + "</option>");
                }
            });
        });
    };

    bindEvents();

    var unbindEvents = function () {
        $("form.uss-form .cus.delete").unbind("click");
    };

    $("form.uss-form .usss.delete").click(function () {
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

        if (symptom_id > 0) {
            $.each(org_symptoms, function (symptom_idx, symptom) {
                if (symptom["id"] == symptom_id) {
                    $.post("/user/" + user_id + "/update_symptom_severities/", {
                        action: "add_cus",
                        symptom_id: symptom_id
                    }, function (res_data) {
                        if (res_data.added) {
                            var tr_template = `
                                <tr>
                                    <td class="align-middle" width="250px">
                                        <h5 class="mb-0">`+ symptom["name"] + `</h5>
                                        <input type="hidden" name="symptom_IDs" value="`+ symptom["id"] + `"/>
                                    </td>
                
                                    <td class="align-middle" width="550px">
                                        <div class="row mx-auto">`;

                            $.each(symptom["levels"], function (level_idx, level) {
                                tr_template += `
                                            <div class="col text-center">
                                                <label for="radio_`+ symptom["id"] + `_` + (level_idx + 1) + `" class="text-center w-100">` + level + `</label>
                                                <input id="radio_`+ symptom["id"] + `_` + (level_idx + 1) + `" type="radio" name="symptom_` + symptom["id"] + `_level" value="` + (level_idx + 1) + `"/>
                                            </div>
                                `;
                            });

                            tr_template += `
                                        </div>
                                    </td>
                
                                    <td class="align-middle" width="250px">
                                        <input name="symptom_`+ symptom["id"] + `_description" class="form-control" placeholder="Description">
                                    </td>
                
                                    <td class="align-middle">
                                        <div class="row mx-auto">
                                            <a class="btn btn-danger delete cus" href="/user/`+ user_id + `/update_symptom_severities/" data-symptom-id="` + symptom["id"] + `">
                                                <i class="fa fa-times" aria-hidden="true"></i>
                                            </a>
                                        </div>
                                    </td>
                                </tr>
                            `;

                            $("table.cus-list tbody").append(tr_template);

                            if (symptom["id"] == symptom_id) {
                                $("form.uss-form select.symptoms option[value=" + symptom["id"] + "]").remove();
                            }

                            unbindEvents();
                            bindEvents();
                        }
                    });
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