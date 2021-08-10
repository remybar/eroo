from django.db import models


RULE_NAME_LENGTH = 255


class Rule(models.Model):
    name = models.CharField(max_length=RULE_NAME_LENGTH)
    website = models.ForeignKey("websites.Website", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
