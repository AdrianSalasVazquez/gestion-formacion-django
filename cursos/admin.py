from django.contrib import admin
from .models import Curso
from django.utils.html import format_html
from datetime import timedelta
from django.utils import timezone

class FiltroFechas(admin.SimpleListFilter):
    title = "Fecha inicio"
    parameter_name = "periodo"

    def lookups(self, request, model_admin):
        return (
            ("hoy", "Hoy"),
            ("manana", "Mañana"),
            ("semana", "Esta semana"),
            ("mes", "Este mes"),
            ("anio", "Este año"),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        hoy = now.date()

        if self.value() == "hoy":
            return queryset.filter(fecha_inicio=hoy)

        if self.value() == "manana":
            mañana = hoy + timedelta(days=1)
            return queryset.filter(fecha_inicio=mañana)

        if self.value() == "semana":
            inicio = hoy - timedelta(days=hoy.weekday())
            fin = inicio + timedelta(days=7)
            return queryset.filter(fecha_inicio__gte=inicio, fecha_inicio__lt=fin)

        if self.value() == "mes":
            inicio = hoy.replace(day=1)
            if hoy.month == 12:
                fin = hoy.replace(year=hoy.year + 1, month=1, day=1)
            else:
                fin = hoy.replace(month=hoy.month + 1, day=1)
            return queryset.filter(fecha_inicio__gte=inicio, fecha_inicio__lt=fin)

        if self.value() == "anio":
            inicio = hoy.replace(month=1, day=1)
            fin = hoy.replace(year=hoy.year + 1, month=1, day=1)
            return queryset.filter(fecha_inicio__gte=inicio, fecha_inicio__lt=fin)

        return queryset

# Register your models here.
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = (
        'miniatura',
        'nombre',
        'profesor',
        'fecha_inicio',
        'fecha_fin',
        'plazas',
        'activo',
    )
    search_fields = (
        'nombre',
        'descripcion',
        'profesor__usuario__first_name',
        'profesor__usuario__last_name',
    )
    list_filter = (
        'activo',
        'plazas',
        FiltroFechas,
    )
    ordering = (
        'nombre',
    )
    fieldsets = (
        (
            'Información General',
            {
                'fields': (
                    'nombre',
                    'descripcion',
                    'profesor',
                )
            }
        ),
        (
            'Planificación',
            {
                'fields': (
                    'fecha_inicio',
                    'fecha_fin',
                    'plazas',
                )
            }
        ),
        (
            'Publicación',
            {
                'fields': (
                    'activo',
                    'imagen',
                )
            }
        ),
    )

    def miniatura(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="80"/>',
                obj.imagen.url
            )
        return '-'
    
    miniatura.short_description = "Imagen"