# Generated by Django 3.2.13 on 2022-07-08 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywords', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='updated',
            field=models.DateTimeField(null=True),
        ),
    ]
