"""
URL configuration for universidad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.models import User  # Importar el modelo User

from django.contrib import admin
from django.urls import path
from portal import views
from django.views.generic import TemplateView
from portal.views import (
    FacultadListView, MateriaListView, ProfesorListView,
    ProfesorDetailView, CursalaView, proponer_facultad, cargar_universidades, cargar_materias, MateriaCreateView, ProfesorCreateView, TodasMateriasListView, TodosProfesoresListView, TopFacultadesView, TopProfesoresView
)

urlpatterns = [
    # Administración
    path('admin/', admin.site.urls),
    
    # Listados generales
    path('', FacultadListView.as_view(), name='facultad_list'),
    path('todas_materias/', TodasMateriasListView.as_view(), name='todas_materias'),
    path('todos_profesores/', TodosProfesoresListView.as_view(), name='todos_profesores'),
    
    # Detalles de facultades, materias y profesores
    path('facultad/<int:pk>/', MateriaListView.as_view(), name='materia_list'),
    path('materia/<int:pk>/', ProfesorListView.as_view(), name='profesor_list'),
    path('profesor/<int:pk>/', ProfesorDetailView.as_view(), name='profesor_detail'),
    
    # Creación de materias y profesores
    path('materia/create/<int:facultad_id>/', MateriaCreateView.as_view(), name='materia_create'),
    path('profesor/create/<int:materia_id>/', ProfesorCreateView.as_view(), name='profesor_create'),
    
    # Vistas de los mejores facultades y profesores
    path('top_facultades/', TopFacultadesView.as_view(), name='top_facultades'),
    path('top_profesores/', TopProfesoresView.as_view(), name='top_profesores'),
    
    # Cursala nosotros
    path('cursala/', CursalaView.as_view(), name='cursala'),
    
    # Mandar Mail
    path('proponer-facultad/', proponer_facultad, name='proponer_facultad'),
    path('propuesta-exitosa/', TemplateView.as_view(template_name='propuesta_exitosa.html'), name='propuesta_exitosa'),
    
    # Comentadas: Carga de datos
    # path('cargar-materias/', cargar_materias, name='cargar_materias'),
    # path('cargar-universidades/', cargar_universidades, name='cargar_universidades'),
    # path('facultad/create/', FacultadCreateView.as_view(), name='facultad_create'),
]
