from django.db import models

class Booking(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
