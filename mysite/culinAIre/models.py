from django.db import models

# Create your models here.
class flavorMetrics(models.Model):
    sweetness = models.FloatField(default=0.0)
    saltiness = models.FloatField(default=0.0)
    spiciness = models.FloatField(default=0.0)
    sourness = models.FloatField(default=0.0)
    bitterness = models.FloatField(default=0.0)
    tanginess = models.FloatField(default=0.0)
    richness = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Total Entries: {self.count}"