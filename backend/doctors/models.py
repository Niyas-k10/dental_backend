from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    image = models.ImageField(upload_to='doctors/')

    def __str__(self):
        return self.name