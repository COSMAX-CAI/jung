from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Patent(models.Model):
    app_number = models.CharField(max_length=100, primary_key=True)
    app_date = models.DateField(null=True)

    app_name = models.CharField(max_length=300)
    title = models.CharField(max_length=500)
    reg_status = models.CharField(max_length=10)

    open_number = models.CharField(max_length=100, null=True)
    open_date = models.DateField(null=True)
    
    pub_number = models.CharField(max_length=100, null=True)
    pub_date = models.DateField(null=True)

    reg_number = models.CharField(max_length=100, null=True)
    reg_date = models.DateField(null=True)

    astr_cont = models.TextField(null=True)

    drawing = models.TextField(null=True)
    big_drawing = models.TextField(null=True)

    keywords= ArrayField(models.CharField(max_length=100), blank=True)

    def __str__(self):
        return f"{self.registration_number}: {self.title}"