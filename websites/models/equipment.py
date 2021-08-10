from django.db import models


EQUIPMENT_NAME_LENGTH = 128
EQUIPMENT_AREA_NAME_LENGTH = 128


class Equipment(models.Model):
    name = models.CharField(max_length=EQUIPMENT_NAME_LENGTH)
    description = models.TextField()

    def __str__(self):
        return self.name


class EquipmentArea(models.Model):
    name = models.CharField(max_length=EQUIPMENT_AREA_NAME_LENGTH)
    website = models.ForeignKey("websites.Website", on_delete=models.CASCADE)
    equipments = models.ManyToManyField(Equipment)

    def __str__(self):
        return self.name
