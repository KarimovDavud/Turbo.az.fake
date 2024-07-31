from django.db import models

class Salon(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    phone = models.CharField(max_length=20)
    ads_count = models.PositiveIntegerField()
    logo = models.ImageField(upload_to='logos/')

    def __str__(self):
        return self.name
