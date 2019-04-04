from django.db import models

# Create your models here.


class Target(models.Model):
    starting_point_url = models.CharField(max_length=200)
    scope = models.CharField(max_length=200)
