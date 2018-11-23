from django.urls import path
from .views import *

urlpatterns = [
    path(
        "connection/",
        base_connection,
        name="base-connection"
    ),

    path(
        "connection/listdb",
        list_db,
        name="list-db"
    ),

    path(
        "connection/<int:id_connection>/check",
        check_connection,
        name="check-connection",
    ),

    path(
        "connection/create",
        ConnectionCreateView.as_view(),
        name="create-connection"
    ),

    path(
        "connection/<int:pk>/edit",
        ConnectionUpdateView.as_view(),
        name="edit-connection",
    ),

    path(
        "connection/list",
        ConnectionListView.as_view(),
        name="list-connections"
    ),

    path(
        "connection/<int:pk>/delete",
        ConnectionDeleteView.as_view(),
        name="delete-connection",
    ),

    path(
        "connection/test",
    ConnectionTestView.as_view(),
    name="test-connection"
    ),

    path(
        "connection/run",
        test_connection,
        name="run-test"
    ),
]
