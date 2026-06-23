from .models import Curso
from .forms import CursoForm
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


# Create your views here.
class ProfesorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.tipo == "profesor"

class ListaCursosView(ListView):
    model = Curso
    template_name = "cursos/lista_cursos.html"
    context_object_name = "cursos"
    paginate_by = 6

    def get_queryset(self):
        queryset = Curso.objects.filter(activo=True)
        buscar = self.request.GET.get("buscar")
        if buscar:
            queryset = queryset.filter(
                Q(nombre__icontains=buscar) | Q(descripcion__icontains=buscar)
            )
        return queryset


class CursoDetailView(DetailView):
    model = Curso
    template_name = "cursos/detalle_curso.html"
    context_object_name = "curso"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class CursoCreateView(LoginRequiredMixin,ProfesorMixin,CreateView):
    form_class = CursoForm
    template_name = "cursos/curso_form.html"
    success_url = reverse_lazy("lista_cursos")


class CursoUpdateView(LoginRequiredMixin,ProfesorMixin,UpdateView):
    form_class = CursoForm
    template_name = "cursos/curso_form.html"
    success_url = reverse_lazy("lista_cursos")


class CursoDeleteView(LoginRequiredMixin,ProfesorMixin,DeleteView):
    model = Curso
    template_name = "cursos/curso_confirm_delete.html"
    success_url = reverse_lazy("lista_cursos")
