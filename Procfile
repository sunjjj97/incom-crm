web: python manage.py migrate --noinput && gunicorn crm_project.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 4

