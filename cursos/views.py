from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Curso
from profesores.models import Profesor
from django.core.paginator import Paginator

# Create your views here.
def lista_cursos(request):

    cursos = Curso.objects.filter(activo=True).select_related(
        'profesor',
        'profesor__usuario'
    ).order_by("fecha_inicio")

    profesores = Profesor.objects.all()

    #Barra de buscador
    busqueda = request.GET.get("buscar", "")
    if busqueda:
        cursos = cursos.filter(
            Q(nombre__icontains=busqueda) | Q(descripcion__icontains=busqueda)
        )

    #Filtro de profesores
    profesor_id = request.GET.get('profesor')
    if profesor_id:
        cursos = cursos.filter(profesor_id=profesor_id)
    
    #Paginación
    paginator = Paginator(cursos,6)
    page_number = request.GET.get('page')
    cursos = paginator.get_page(page_number)

    return render(
        request,
        "cursos/lista_cursos.html",
        {
            "cursos": cursos,
            'profesores': profesores,
            "total_cursos": paginator.count
        },
    )


def detalle_curso(request, slug):

    curso = get_object_or_404(Curso, slug=slug, activo=True)

    ocupadas = curso.matriculas.count()

    return render(
        request, "cursos/detalle_curso.html", {"curso": curso, "ocupadas": ocupadas}
    )
