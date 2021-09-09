# Architecture

- domaine `eroo.fr`
- mail: sendgrid + OVH: `contact@eroo.fr`
- hosting sur heroku avec 2 workers : le serveur web + celery
- sentry pour les erreurs/exceptions
- database: postgres
- storage des assets : Amazon S3
- logging: logentries
- google map: via gcp remy.baranx@gmail.com (Map Javascript API)

# Celery

- use Redis as message broker:
    `redis-cli ping` checks that Redis server is running

- start the worker process
    `celery -A eroo worker -l info` 

- test that the Celery task scheduler is ready for action:
    `celery -A eroo beat -l info`

- use `django-celery-results` to store tasks results in the database (backend)

# Heroku

- voir les apps: `heroku apps`

- sélectionner une app: `heroku git:remote -a YOUR_APP`

- voir les logs: `heroku logs [-d dynoname]` 

- voir l'état des dynos: `heroku ps`
