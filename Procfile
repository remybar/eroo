release: python3 manage.py migrate
web: gunicorn eroo.wsgi --preload --log-file -
worker: celery -A eroo worker -l info -B
