$(document).ready(function () {

    $("#button_schema").click(function () {
        $.ajax({
            url: $("#url").val(),
            type: "POST",
            data: $("#form_service").serialize(),
            beforeSend: function () {
                $("#loader").show();
            },
            success: function (data) {
                $("#loader").hide();
                $("#button_schema").hide();
                $("#table_type").show();
                $("#button_save").show();

                $("#name_type").html($("#id_type_name").val());
                $("#fields_type").empty();
                $("#id_unique_key").empty();
                $("#id_unique_key").append(
                    "<option value='' selected>-----------</option>"
                );
                data.object_list.forEach(element => {
                    $("#fields_type").append(
                        "<tr>\
                            <td>"+ element + "</td>\
                            <td><input type='text' class='form-control' id='"+ element + "'></td>\
                        </tr>"
                    );
                    $("#id_unique_key").append(
                        "<option value=" + element + ">" + element + "</option>"
                    );
                });
            },

            error: function () {
                $("#loader").hide();
                $("#alert_error").show().hide(2000);
            }
        });

    });

    $("#id_type_name").keydown(function () {
        $("#table_type").hide();
        $("#button_save").hide();
        $("#button_schema").show();
    });

    $("#id_query_sql").keydown(function () {
        $("#table_type").hide();
        $("#button_save").hide();
        $("#button_schema").show();
    });

    $("#id_connection").change(function () {
        $("#table_type").hide();
        $("#button_save").hide();
        $("#button_schema").show();
    });

    $("#form_service").submit(function (evt) {
        var dict = {};
        $("#fields_type input").each(function () {
            if ($(this).val() != "") {
                dict[String($(this).id())] = $(this).val();
            }
        });
        $("#id_description_fields").val(dict);
    });

});