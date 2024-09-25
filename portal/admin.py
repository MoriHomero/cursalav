from django.contrib import admin
from .models import Facultad, Materia, Profesor, Comentario

admin.site.register(Facultad)
admin.site.register(Materia)
admin.site.register(Profesor)
admin.site.register(Comentario)