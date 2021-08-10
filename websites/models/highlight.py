from django.db import models


HIGHLIGHT_TITLE_LENGTH = 255


class Highlight(models.Model):
    title = models.CharField(max_length=HIGHLIGHT_TITLE_LENGTH)
    message = models.TextField()
    website = models.ForeignKey("websites.Website", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
