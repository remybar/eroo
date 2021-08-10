from django.db import models

from websites.utils import get_review_dir_path

AUTHOR_NAME_LENGTH = 64
LANGUAGE_LENGTH = 8


class Review(models.Model):
    author_name = models.CharField(max_length=AUTHOR_NAME_LENGTH)
    author_picture = models.ImageField(upload_to=get_review_dir_path)
    review = models.TextField()
    date = models.DateField()
    language = models.CharField(max_length=LANGUAGE_LENGTH)
    website = models.ForeignKey("websites.Website", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author_name} ({self.date})"

    def picture_url(self):
        return self.author_picture.url
