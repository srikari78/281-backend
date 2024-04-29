from django.db import models
#for using AI models
import torch 


# Create your models here.
class Device(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    altitude = models.FloatField()
    dist_id = models.CharField(max_length=12)
    video_url = models.URLField(blank=True, null=True)  
    status = models.CharField(max_length=15)

    
    class Meta:
        db_table = 'drones'

def load_models():
    best_model_path = 'models/best.pt'
    emr_incident_model_path = 'models/Emr&Incident_Model_V11_best.pt'
    
    best_model = torch.load(best_model_path)
    emr_incident_model = torch.load(emr_incident_model_path)
    
    best_model.eval()
    emr_incident_model.eval()
    
    return best_model, emr_incident_model