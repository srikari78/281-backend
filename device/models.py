from django.db import models

# Create your models here.
class Device(models.Model):
    drone_id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    altitude = models.FloatField()
    district_id = models.CharField(max_length=12)
    enabled = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'drones'