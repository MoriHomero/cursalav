from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Sum, Count
from decimal import Decimal
from django.db.models import Avg, Q, F

# Modelo para Facultades

class Facultad(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre

    def promedio_profesores(self):
        promedio = Profesor.objects.filter(materias__facultad=self).aggregate(promedio=Avg('comentarios__puntaje'))['promedio']
        return round(promedio, 2) if promedio is not None else None

    @staticmethod
    def top_facultades():
        facultades = Facultad.objects.annotate(
            total_promedio=Avg(
                'materias__profesores__comentarios__puntaje',
                filter=Q(materias__profesores__comentarios__isnull=False)
            ),
            total_comentarios=Count(
                'materias__profesores__comentarios',
                filter=Q(materias__profesores__comentarios__isnull=False)
            )
        ).order_by('-total_promedio').filter(total_promedio__isnull=False)[:10]

        for facultad in facultades:
            facultad.total_promedio = round(facultad.total_promedio, 2)
        return facultades
    

# Modelo para Materias
class Materia(models.Model):
    nombre = models.CharField(max_length=255)
    facultad = models.ForeignKey(Facultad, related_name='materias', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('nombre', 'facultad')  # Añadido unique_together para evitar duplicados

    def __str__(self):
        return self.nombre

# Modelo para Profesores
class Profesor(models.Model):
    nombre = models.CharField(max_length=255)
    materias = models.ManyToManyField(Materia, related_name='profesores')
    facultades = models.ManyToManyField(Facultad, related_name='profesores', blank=True)

    def __str__(self):
        return self.nombre

    def promedio(self):
        promedio = self.comentarios.aggregate(promedio=Avg('puntaje'))['promedio']
        return round(promedio, 2) if promedio is not None else None

    @staticmethod
    def top_profesores(facultad_id=None):
        queryset = Profesor.objects.annotate(
            promedio=Avg('comentarios__puntaje'),
            votos=Count('comentarios')
        ).filter(promedio__isnull=False)
        
        if facultad_id:
            queryset = queryset.filter(facultades__id=facultad_id)
        
        profesores = queryset.order_by('-promedio')[:10]
        for profesor in profesores:
            profesor.promedio = round(profesor.promedio, 2)
        return profesores

# Modelo para Comentarios
class Comentario(models.Model):
    texto = models.TextField()
    puntaje = models.DecimalField(
        max_digits=4,  # Total de dígitos, incluyendo decimales
        decimal_places=2,  # Número de decimales
        validators=[MinValueValidator(Decimal('1.00')), MaxValueValidator(Decimal('10.00'))]
    )
    profesor = models.ForeignKey(Profesor, related_name='comentarios', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profesor.nombre}: {self.puntaje}"
    
class PropuestaFacultad(models.Model):
    nombre_universidad = models.CharField(max_length=200)
    mensaje = models.TextField(blank=True)
    email_contacto = models.EmailField()  # Nuevo campo para el email de contacto
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_universidad