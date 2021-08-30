release: python3 manage.py migrate
web: gunicorn eroo.wsgi --preload --log-file -
celery: celery worker -A eroo -l info -c 4
