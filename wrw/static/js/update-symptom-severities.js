$(document).ready(function () {
    var showAlert = function (msg) {
        $(".alert strong").text(msg);
        $(".alert").addClass("show");

        setTimeout(function () {
            $(".alert").removeClass("show");
        }, 500);

    };

    $("form.uss-form .cus.delete").click(function (e) {
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
            window.location.href = "/user/" + user_id + "/update_symptom_severities/?action=add_cus&symptom_id=" + symptom_id;
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