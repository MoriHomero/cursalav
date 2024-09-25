const universidades = document.getElementById('unibtn');
const profesores = document.getElementById('profebtn');
const materias = document.getElementById('matebtn');

universidades.addEventListener('click', () => {
    window.location.href = "{% url 'facultad_list' %}";
});

profesores.addEventListener('click', () => {
    window.location.href = "{% url 'todos_profesores' %}";
});

materias.addEventListener('click', () => {
    window.location.href = "{% url 'todas_materias' %}";
});
