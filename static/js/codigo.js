$(document).ready(function () {

    check_connection();

    $("#list_db").click(function () {
        $.ajax({
            url: $("#url").val(),
            type: "POST",
            data: $("#form_connection").serialize(),
            beforeSend: function () {
                $("#loader").show();
            },
            success: function (data) {
                if (data.object_list) {
                    $("#id_dbname").html("<option value='' selected disabled>Selecione una base de datos</option>");
                    data.object_list.forEach(element => {
                        $("#id_dbname").append(
                            "<option value='" + element + "'>" + element + "</option>"
                        );
                    });
                    $("#loader").hide();
                    Lobibox.notify('success', {
                        msg: 'Lorem ipsum dolor sit amet against apennine any created, spend loveliest, building stripes.'
                    });
                } else {
                    $("#loader").hide();
                    Lobibox.notify('error', {
                        msg: 'Lorem ipsum dolor sit amet against apennine any created, spend loveliest, building stripes.'
                    });
                }
            },

            error: function () {
                $("#loader").hide();
                Lobibox.notify('error', {
                    msg: 'Lorem ipsum dolor sit amet against apennine any created, spend loveliest, building stripes.'
                });
            }
        });

    });

    $("#id_manager_db").change(function () {
        switch ($(this).val()) {
            case "mysql":
                $("#id_port").val(3306);
                break;

            case "postgresql":
                $("#id_port").val(5432);
                break;

            case "oracle":
                $("#id_port").val(1521);
                break;
        }
    });

    $("input[id]").keydown(function () {
        $("#id_dbname").html("<option value='' selected disabled>Selecione una base de datos</option>");
        $("#button_list").show();
        $("#button_save").hide();
    });

    $("#id_connection_name").keydown(function () {
        $("#alert_error_connection_name").hide();
    });

    $("#id_manager_db").change(function () {
        $("#id_dbname").html("<option value='' selected disabled>Selecione una base de datos</option>");
        $("#button_list").show();
        $("#button_save").hide();
    });

    $("#refresh_state_connections").click(function () {
        check_connection();
    });

    $("#form_test").submit(function (evt) {
        evt.preventDefault();
        $.ajax({
            url: $("#url").val(),
            type: "POST",
            data: $("#form_test").serialize(),
            beforeSend: function () {

            },
            success: function (data) {
                $("#result_query").html(data);
            },

            error: function () {
            }
        });
    });

    $('#basicSuccess').on('click', function () {
        Lobibox.notify('success', {
            msg: 'Lorem ipsum dolor sit amet against apennine any created, spend loveliest, building stripes.'
        });
    });
});

function check_connection() {
    $("td[id]").each(function (index, element) {
        $.ajax({
            url: "/connection/" + $(this).attr("id") + "/check",
            type: "GET",
            success: function (data) {
                if (data.object == true) {
                    $(element).html("<center>" +
                        "<span class='glyphicon glyphicon-ok-circle label-success'></span>" +
                        "</center>");
                } else {
                    $(element).html("<center>" +
                        "<span class='glyphicon glyphicon-remove-circle label-danger'></span>" +
                        "</center>");
                }
            },
            error: function () {
                $(element).html("<center>" +
                    "<span class='glyphicon glyphicon-remove-circle label-danger'></span>" +
                    "</center>");
            }
        });
    });
}

function check_delete_connection(url, nombre, motor, usuario) {
    $("#spn_nombre").html(nombre);
    $("#spn_motor").html(motor);
    $("#spn_usuario").html(usuario);
    $("#form_confirmacion").attr('action', url);
    $("#mostrarmodal").modal("show");
}

