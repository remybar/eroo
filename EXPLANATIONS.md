# Celery

- use Redis as message broker:
    `redis-cli ping` checks that Redis server is running

- start the worker process
    `celery -A eroo worker -l info` 

- test that the Celery task scheduler is ready for action:
    `celery -A eroo beat -l info`

- use `django-celery-results` to store tasks results in the database (backend)
