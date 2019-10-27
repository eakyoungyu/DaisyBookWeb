from django.db import models


class Book(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    start_page = models.IntegerField(default=1)
    end_page = models.IntegerField()
    is_poem = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)