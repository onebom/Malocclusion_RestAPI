import os
from django.utils import timezone
from django.db import models
from .mmmil.utils.postprocessing import malocclusion_result
import cv2 as cv
from django.contrib.auth.models import User # 계정 관련 모델.



import threading

ds_lock = threading.Lock()


'''
저장 경로 함수 설정
'''
def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    return f"{now:%Y%m%d}/{filename}"


'''
Treatment DB 선언 부분
'''


class Treatment(models.Model):

    id = models.BigAutoField(primary_key=True)

    Medical_image = models.ImageField(upload_to = upload_to, blank=True)
    Medical_image1 = models.ImageField(upload_to = upload_to, blank=True)
    Medical_image2 = models.ImageField(upload_to = upload_to, blank=True)


    prediction_result = models.CharField(max_length=46*5, default='None')

    # ip = models.GenericIPAddressField(null=True, editable=False)

    class Meta:
        ordering = ('id',)

    #@async_to_sync
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ds_lock.acquire()
        malocclusion_predict = malocclusion_result(self.Medical_image.path)
        ds_lock.release()
        self.prediction_result = f'{malocclusion_predict}'

        super().save(force_update=True)
