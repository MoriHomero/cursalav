from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Facultad, Materia, Profesor, Comentario
from .forms import ComentarioForm, FacultadForm, MateriaForm, ProfesorForm
from django.urls import reverse
from django.db.models import Q
from django.db.models import Prefetch
from django.views.generic import TemplateView
from django.urls import reverse_lazy
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import Facultad
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import json
from django.core.paginator import Paginator
from .models import Facultad, Materia
from django.contrib import messages 
from .forms import PropuestaFacultadForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect

def proponer_facultad(request):
    if request.method == 'POST':
        form = PropuestaFacultadForm(request.POST)
        if form.is_valid():
            propuesta = form.save()

            # Enviar mail
            send_mail(
                subject=propuesta.nombre_universidad,  # El nombre de la universidad como asunto
                message=(
                    f'Se ha propuesto una nueva universidad: {propuesta.nombre_universidad}.\n'
                    f'Mensaje adicional: {propuesta.mensaje}\n'
                    f'Email de contacto: {propuesta.email_contacto}'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['morihomero@gmail.com'],  # El correo que recibe el mensaje
                fail_silently=False,
            )
            return redirect('propuesta_exitosa')
    else:
        form = PropuestaFacultadForm()
    
    return render(request, 'proponer_facultad.html', {'form': form})


# Vista para insertar materias desde una solicitud POST
def cargar_materias(request):
    data = [
        {"facultad_id": 1, "materias": ["Matemática", "Física", "Química"]},
        {"facultad_id": 2, "materias": ["Programación", "Sistemas Operativos", "Redes"]},
        {"facultad_id": 3, "materias": ["Sociología", "Antropología", "Economía"]},
        {"facultad_id": 4, "materias": ["Pintura", "Escultura", "Música"]},
        {"facultad_id": 5, "materias": ["Historia", "Literatura", "Filosofía"]},
        {"facultad_id": 6, "materias": ["Biología", "Ecología", "Genética"]},
        {"facultad_id": 7, "materias": ["Derecho", "Política", "Relaciones Internacionales"]},
        {"facultad_id": 8, "materias": ["Marketing", "Finanzas", "Recursos Humanos"]},
        {"facultad_id": 9, "materias": ["Psicología", "Sociología", "Trabajo Social"]},
        {"facultad_id": 10, "materias": ["Contabilidad", "Administración", "Economía"]},
        {"facultad_id": 11, "materias": ["Ingeniería Civil", "Arquitectura", "Diseño"]},
        {"facultad_id": 12, "materias": ["Medicina", "Enfermería", "Fisioterapia"]},
        {"facultad_id": 13, "materias": ["Teología", "Filosofía", "Historia"]},
        {"facultad_id": 14, "materias": ["Derecho Penal", "Derecho Civil", "Derecho Comercial"]},
        {"facultad_id": 15, "materias": ["Ciencia Política", "Economía", "Sociología"]},
        {"facultad_id": 16, "materias": ["Astronomía", "Geología", "Meteorología"]}
    ]

    for item in data:
        facultad_id = item["facultad_id"]
        facultad = Facultad.objects.get(id=facultad_id)
        for materia_nombre in item["materias"]:
            Materia.objects.create(nombre=materia_nombre, facultad=facultad)

    try:
        for item in data:
            facultad_id = item["facultad_id"]
            facultad = Facultad.objects.get(id=facultad_id)

            for materia_nombre in item["materias"]:
                Materia.objects.create(nombre=materia_nombre, facultad=facultad)

        return HttpResponse("Materias cargadas con éxito.")
    
    except Facultad.DoesNotExist:
        return HttpResponse("Error: No se encontró una Facultad con el ID especificado.")


# Vista para insertar universidades desde una solicitud POST
def cargar_universidades(request):
    data = [
        {"nombre": "Universidad de Buenos Aires (UBA)"},
        {"nombre": "Universidad Nacional de La Plata (UNLP)"},
        {"nombre": "Universidad Tecnológica Nacional (UTN)"},
        {"nombre": "Universidad Católica Argentina (UCA)"},
        {"nombre": "Universidad del Salvador (USAL)"},
        {"nombre": "Universidad de Palermo (UP)"},
        {"nombre": "Universidad de Ciencias Empresariales y Sociales (UCES)"},
        {"nombre": "Universidad Argentina de la Empresa (UADE)"},
        {"nombre": "Universidad de Belgrano (UB)"}
    ]

    for item in data:
        Facultad.objects.create(nombre=item["nombre"])

    return HttpResponse("Universidades cargadas con éxito.")

# Listar todas las facultades
class FacultadListView(ListView):
    model = Facultad
    template_name = 'facultad_list.html'
    context_object_name = 'facultades'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))
        return queryset

# Listar todas las materias de una facultad
class MateriaListView(ListView):
    model = Materia
    template_name = 'materia_list.html'
    context_object_name = 'materias'
    paginate_by = 20

    def get_queryset(self):
        queryset = Materia.objects.filter(facultad__id=self.kwargs['pk'])
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facultad'] = Facultad.objects.get(pk=self.kwargs['pk'])
        return context

# Listar todos los profesores de una materia
class ProfesorListView(ListView):
    model = Profesor
    template_name = 'profesor_list.html'
    context_object_name = 'profesores'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Profesor.objects.filter(materias__id=self.kwargs['pk'])
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materia'] = Materia.objects.get(pk=self.kwargs['pk'])
        return context
    
# Detalle de un profesor con opción para añadir comentarios
class ProfesorDetailView(DetailView, CreateView):
    model = Profesor
    template_name = 'profesor_detail.html'
    context_object_name = 'profesor'
    form_class = ComentarioForm
    paginate_by = 5  # Número de comentarios por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comentarios = self.get_object().comentarios.all()
        paginator = Paginator(comentarios, self.paginate_by)

        page = self.request.GET.get('page')
        comentarios_paginados = paginator.get_page(page)

        context['comentarios'] = comentarios_paginados
        return context

    def form_valid(self, form):
        form.instance.profesor = self.get_object()
        form.save()
        return redirect(reverse('profesor_detail', kwargs={'pk': self.get_object().pk}))

# Crear una nueva facultad
class FacultadCreateView(CreateView):
    model = Facultad
    form_class = FacultadForm
    template_name = 'facultad_form.html'
    success_url = '/'

# Crear una nueva materia
class MateriaCreateView(CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'materia_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        facultad = get_object_or_404(Facultad, pk=self.kwargs['facultad_id'])
        kwargs['facultad'] = facultad
        return kwargs

    def get_success_url(self):
        return reverse_lazy('materia_list', kwargs={'pk': self.kwargs['facultad_id']})

# Crear un nuevo profesor
class ProfesorCreateView(CreateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'profesor_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['materia'] = get_object_or_404(Materia, pk=self.kwargs.get('materia_id'))
        return kwargs

    def form_valid(self, form):
        # Guarda el profesor
        response = super().form_valid(form)

        if form.cleaned_data.get('existing_profesor'):
            messages.info(self.request, f'El profesor "{form.cleaned_data["existing_profesor"].nombre}" ya existía y ha sido añadido a la materia.')
        else:
            messages.success(self.request, 'El profesor ha sido agregado exitosamente.')

        # Redirige a la lista de profesores de la materia
        return self.redirect_to_success_url()

    def redirect_to_success_url(self):
        materia_id = self.kwargs.get('materia_id')
        success_url = reverse('profesor_list', args=[materia_id])
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        # No se llama directamente pero es necesario
        return reverse('profesor_list', args=[self.kwargs.get('materia_id')])
    
class TodasMateriasListView(ListView):
    model = Materia
    template_name = 'todas_materias.html'
    context_object_name = 'materias'
    paginate_by = 10  # Número de materias por página

    def get_queryset(self):
        queryset = Materia.objects.all().distinct().order_by('nombre')  
        facultad_id = self.request.GET.get('facultad')
        profesor_id = self.request.GET.get('profesor')
        
        if facultad_id:
            queryset = queryset.filter(facultad_id=facultad_id)
        if profesor_id:
            queryset = queryset.filter(profesores__id=profesor_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facultades'] = Facultad.objects.all().order_by('nombre')
        context['profesores'] = Profesor.objects.all().order_by('nombre')  
        return context


    
class TodosProfesoresListView(ListView):
    model = Profesor
    template_name = 'todos_profesores.html'
    context_object_name = 'profesores'
    paginate_by = 10  # Número de profesores por página

    def get_queryset(self):
        queryset = Profesor.objects.all().distinct().order_by('nombre')  # Order by a relevant field
        materia_id = self.request.GET.get('materia')
        facultad_id = self.request.GET.get('facultad')
        
        if materia_id:
            queryset = queryset.filter(materias__id=materia_id).distinct()
        if facultad_id:
            queryset = queryset.filter(facultades__id=facultad_id).distinct()
            
        return queryset.prefetch_related('facultades').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materias'] = Materia.objects.select_related('facultad').values('id', 'nombre', 'facultad__nombre').distinct()
        context['facultades'] = Facultad.objects.all().order_by('nombre')
        return context

    
# Listar las mejores facultades
class TopFacultadesView(TemplateView):
    template_name = 'top_facultades.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facultades'] = Facultad.top_facultades()
        return context

# Listar los mejores profesores
class TopProfesoresView(TemplateView):
    template_name = 'top_profesores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        facultad_id = self.request.GET.get('facultad')
        context['facultades'] = Facultad.objects.all()
        context['profesores'] = Profesor.top_profesores(facultad_id)
        return context
    
#Cursla nosotros
class CursalaView(TemplateView):
    template_name = 'cursala.html'