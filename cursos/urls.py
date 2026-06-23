from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.ListaCursosView.as_view(),
        name='lista_cursos'
    ),
    path(
        '<slug:slug>/',
        views.CursoDetailView.as_view(),
        name='detalle_curso'
    ),
]