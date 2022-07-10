from django.db import models

# Create your models here.

class Keyword(models.Model):
    keyword = models.CharField(max_length=100, primary_key=True)
    updated = models.DateTimeField(null=True)

    def __str__(self):
        return self.keyword