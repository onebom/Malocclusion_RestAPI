import os
from django.utils import timezone
from django.db import models
from .mmmil.utils.postprocessing import malocclusion_result
import cv2 as cv
#from asgiref.sync import async_to_sync
import threading

ds_lock = threading.Lock()

def upload_to(instance, filename):

    return f"{filename}"

class DeepLearningModelInference(models.Model):

    id= models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=200, blank=False, default='')
    Medical_image = models.ImageField(upload_to = upload_to, blank=True)
    prediction_result = models.CharField(max_length=46*5, default='None')
    # ip = models.GenericIPAddressField(null=True, editable=False)

    class Meta:
        ordering = ('name',)

    #@async_to_sync
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ds_lock.acquire()
        malocclusion_predict = malocclusion_result(self.Medical_image.path)
        ds_lock.release()
        self.prediction_result = f'{malocclusion_predict}'
        super().save(force_update=True)
