from django import forms
from .models import Comentario, Facultad, Materia, Profesor, PropuestaFacultad
from django.core.exceptions import ValidationError
import re
import Levenshtein
import unicodedata

def normalize_name(name):
    # Quitar espacios, puntos y hacer que todo sea minúsculas
    return re.sub(r'[\s\.]', '', name).lower()

def has_common_substring(name1, name2, min_length=7):
    # Verifica si hay una subcadena común de al menos min_length caracteres entre name1 y name2
    for i in range(len(name1) - min_length + 1):
        substring = name1[i:i + min_length]
        if substring in name2:
            return True
    return False

# Formulario para comentarios
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto', 'puntaje']

# Formulario para facultades
class FacultadForm(forms.ModelForm):
    class Meta:
        model = Facultad
        fields = ['nombre']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        normalized_name = normalize_name(nombre)
        if Facultad.objects.filter(nombre__iexact=normalized_name).exists():
            raise ValidationError('Ya existe una facultad con este nombre.')
        return nombre

# Formulario para materias
class MateriaForm(forms.ModelForm):
    facultad_nombre = forms.CharField(label='Facultad', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Materia
        fields = ['nombre', 'facultad_nombre']

    def __init__(self, *args, facultad=None, **kwargs):
        super().__init__(*args, **kwargs)
        if facultad:
            self.fields['facultad_nombre'].initial = facultad.nombre
        self.facultad = facultad

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        normalized_nombre = normalize_name(nombre)

        # Buscar materias en la misma facultad
        materias_existentes = Materia.objects.filter(facultad=self.facultad)

        umbral_similitud = 2  # Puedes ajustar este valor según la tolerancia que desees

        for materia in materias_existentes:
            normalized_materia_nombre = normalize_name(materia.nombre)
            distancia = Levenshtein.distance(normalized_nombre, normalized_materia_nombre)

            # Verificar si las materias tienen nombres similares pero números diferentes
            if distancia <= umbral_similitud:
                # Comprobar si los números son diferentes
                nombre_sin_numeros = re.sub(r'\d+', '', nombre).strip().lower()
                materia_nombre_sin_numeros = re.sub(r'\d+', '', materia.nombre).strip().lower()

                if nombre_sin_numeros == materia_nombre_sin_numeros:
                    # Comparar los números
                    numero_actual = re.search(r'\d+', nombre)
                    numero_existente = re.search(r'\d+', materia.nombre)
                    
                    if numero_actual and numero_existente:
                        if numero_actual.group() != numero_existente.group():
                            # Números diferentes, así que es una materia válida
                            continue
                    raise forms.ValidationError(
                        'Ya existe una materia con un nombre similar en esta facultad. '
                        'Por favor, elige un nombre diferente.'
                    )

        return nombre

    def save(self, commit=True):
        materia = super().save(commit=False)
        if self.facultad:
            materia.facultad = self.facultad
        if commit:
            materia.save()
        return materia

# Formulario para profesores
class ProfesorForm(forms.ModelForm):
    materia_nombre = forms.CharField(label='Materia', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Profesor
        fields = ['nombre', 'materia_nombre']

    def __init__(self, *args, materia=None, **kwargs):
        super().__init__(*args, **kwargs)
        if materia:
            self.fields['materia_nombre'].initial = materia.nombre
        self.materia = materia
        self.existing_profesor = None

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        normalized_name = normalize_name(nombre)
        profesores = Profesor.objects.all()

        for profesor in profesores:
            if (normalize_name(profesor.nombre) == normalized_name or 
                has_common_substring(normalized_name, normalize_name(profesor.nombre))):
                if profesor.materias.filter(id=self.materia.id).exists():
                    raise ValidationError('Este profesor ya está asignado a esta materia.')
                self.existing_profesor = profesor
                return nombre

        return nombre

    def save(self, commit=True):
        if self.existing_profesor:
            profesor = self.existing_profesor
            profesor.materias.add(self.materia)
            profesor.facultades.add(self.materia.facultad)
        else:
            profesor = super().save(commit=False)
            if commit:
                profesor.save()
                profesor.materias.set([self.materia])
                facultades = set(materia.facultad for materia in profesor.materias.all())
                profesor.facultades.set(facultades)
        return profesor

class PropuestaFacultadForm(forms.ModelForm):
    class Meta:
        model = PropuestaFacultad
        fields = ['nombre_universidad', 'mensaje', 'email_contacto']
        labels = {
            'nombre_universidad': '',
            'mensaje': '',
            'email_contacto': '',
        }
        widgets = {
            'nombre_universidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la universidad'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba su mensaje aquí', 'rows': 4}),
            'email_contacto': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su email de contacto'}),
        }