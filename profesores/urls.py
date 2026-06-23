from django.urls import path
from . import views

urlpatterns = [
    path(
        'dashboard/',
        views.dashboard_profesor,
        name='dashboard_profesor'
    ),
    path(
        'mis-cursos/',
        views.mis_cursos_profesor,
        name='mis_cursos_profesor'
    ),
]