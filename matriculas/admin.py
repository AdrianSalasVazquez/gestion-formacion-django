from django.contrib import admin
from .models import Matricula

# Register your models here.
@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = (
        'alumno',
        'curso',
        'fecha_matricula',
    )
    search_fields = (
        'alumno__username',
        'curso__nombre',
    )
    ordering = (
        '-fecha_matricula',
    )