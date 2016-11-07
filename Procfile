web: gunicorn fm_proj.wsgi --log-file - --workers=2
worker: python manage.py celery worker -B -l info
