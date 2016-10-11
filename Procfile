web: gunicorn fm_proj.wsgi --log-file - --workers=2
main_worker: python manage.py celery worker --beat --loglevel=info
