from django.db import models


class Book(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    image_dir = models.TextField()
    txt_dir = models.TextField()
    start_page = models.IntegerField(default=1)
    end_page = models.IntegerField()
    is_poem = models.BooleanField(default=False)
    test_image = models.FileField(blank=True, null=True)


class Images(models.Model):
    image = models.FileField(null=True, blank=True)
