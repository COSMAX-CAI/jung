from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Patent(models.Model):
    registration_number = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    abstract = models.TextField()
    keywords= ArrayField(models.CharField(max_length=100), blank=True)

    def __str__(self):
        return f"{self.registration_number}: {self.title}"