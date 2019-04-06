$(document).ready(function () {
    $("#id_authentication").change(function () {
        if ($(this).val() == 1) {
            $("#dn_template").show();
            $("#user_search").hide();
        } else {
            $("#dn_template").hide();
            $("#user_search").show();
        }
    });

    $("#set_backend_setting_ldap_auth").click(function () {
        $.ajax({
            url: $("#url_authldap_backend_set").val(),
            type: "POST",
            beforeSend: function () {
                $("#loader").show();
            },
            success: function (data) {
                $("#loader").hide();
                $("#modal_confirmation_change_success").modal('show');
                location.reload();
            },
            error: function () {
                $("#loader").hide();
                $("#modal_confirmation_change_error").modal('show');
            }
        });
    });

    $("#set_backend_setting_authdb").click(function () {
        $.ajax({
            url: $("#url_backend_setting_authdb").val(),
            type: "POST",
            beforeSend: function () {
                $("#loader").show();
            },
            success: function (data) {
                $("#loader").hide();
                $("#modal_confirmation_change_success").modal('show');
                location.reload();
            },

            error: function () {
                $("#loader").hide();
                $("#modal_confirmation_change_error").modal('show');
            }
        });
    });

    $('#default-primary').click(function () {
        new PNotify({
            title: 'Regular Notice',
            text: 'Check me out! I\'m a notice.',
            type: 'custom',
            addclass: 'notification-primary',
            icon: 'fa fa-twitter'
        });
    });

    $("input").keydown(function () {
        $("#options").show();
    });
});

function reload() {
    location.reload();
}

function open_modal_user_search(url) {
    $('#modal_create_user_search').load(url, function () {
        $(this).modal('show');
    });
    return false;
}

function close_modal() {
    $('#popup').modal('hide');
    return false;
}

function check_delete_user_search(url, dn_base, filter_attr) {
    $("#dn_base").html(dn_base);
    $("#filter_attr").html(filter_attr);
    $("#form_delete_user_search").attr('action', url);
    $("#modal_delete_user_search").modal("show");
}
