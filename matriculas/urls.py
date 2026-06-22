from django.urls import path
from . import views
urlpatterns = [
    path(
        "matricular/<int:curso_id>/",
        views.matricularse,
        name="matricularse"
    ),
    path(
        "mis-cursos/",
        views.mis_cursos,
        name="mis_cursos"
    ),
]