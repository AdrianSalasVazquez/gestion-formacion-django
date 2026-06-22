from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cursos.models import Curso
from .models import Matricula


# Create your views here.
@login_required
def matricularse(request, curso_id):

    curso = get_object_or_404(Curso, pk=curso_id, activo=True)

    if request.user.tipo != "alumno":
        messages.error(request, "Sólo los alumnos pueden matricularse.")
        return redirect("detalle_curso", curso.id)

    inscritos = curso.matriculas.count()
    if inscritos >= curso.plazas:
        messages.error(request, "No quedan plazas.")
        return redirect("detalle_curso", curso.id)

    matricula, creada = Matricula.objects.get_or_create(
        alumno=request.user, curso=curso
    )

    if creada:
        messages.success(request, "Matrícula realizada correctamente.")
    else:
        messages.warning(request, "Ya estás matriculado en este curso.")
    return redirect("detalle_curso", curso.id)


@login_required
def mis_cursos(request):

    matriculas = Matricula.objects.filter(alumno=request.user).select_related("curso")

    return render(request, "matriculas/mis_cursos.html", {"matriculas": matriculas})
