#!/usr/bin/env bash

set -o errexit

# Instala las dependencias
pip install -r requirements.txt

# Aplica las migraciones primero
python manage.py migrate

# Recoge archivos estáticos
python manage.py collectstatic --noinput

# Crea el superusuario si no existe
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin1234') if not User.objects.filter(username='admin').exists() else print('Admin user already exists')"
