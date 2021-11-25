import os
from django.utils import timezone
from django.db import models
from .mmmil.utils.postprocessing import malocclusion_result
import cv2 as cv
#from asgiref.sync import async_to_sync
import threading

ds_lock = threading.Lock()

def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    return f"{now:%Y%m%d}/{filename}"


class DeepLearningModelInference(models.Model):
    CLR_EXT_LIST = [(0, 'Clear Aligner'), (1, 'Extraction'), (-1, 'Not-defined')]
    MALOCCLUSION_CLASS_LIST = [(1, 'CLASS-1'), (2, 'CLASS-2'), (3, 'CLASS-3'), (-1, 'Not-defined')]
    extraction = [(0, 'non extraction'), (1, 'extraction on upper')]
    surgery = [(0,'non Surgery'),(1,'Surgery')]

    treatment_id = models.CharField(max_length=46*5, blank=False, default='')
    id = models.BigAutoField(primary_key=True)
    treatment_state = models.IntegerField('Treatment state', default=0,
                               help_text='치료전:0 / 치료후:1',
                               choices=[(0, 'Pre'),
                                        (1, 'Post')])  # 치료후 데이터인지.

    Treatment_Type = models.IntegerField('Treatment Type',default=-1,choices=CLR_EXT_LIST)


    Angle_class_type_left = models.IntegerField('Angle class type left',default = -1, choices=MALOCCLUSION_CLASS_LIST)
    Angle_class_dist_left = models.FloatField('Angle distance left(mm)',default = 0)
    Angle_class_type_right = models.IntegerField('Angle class type right', default = -1,choices=MALOCCLUSION_CLASS_LIST)
    Angle_class_dist_right= models.FloatField('Angle distance right(mm)',default=0)
    extraction_upper = models.IntegerField('Extraction Upper', default=0, choices=extraction)
    extraction_lower = models.IntegerField('Extraction Lower', default=0, choices=extraction)
    Surgery_upper = models.IntegerField('Surgery Upper', default=0, choices=surgery)
    Surgery_lower = models.IntegerField('Surgery Lower', default=0, choices=surgery)

    Medical_image = models.ImageField(upload_to = upload_to, blank=True)


    prediction_result = models.CharField(max_length=46*5, default='None')
    prediction_Angle_class_type_left = models.IntegerField('Prediction Angle class type left',default = -1, choices=MALOCCLUSION_CLASS_LIST)
    prediction_Angle_class_type_right = models.IntegerField('Prediction Angle class type right',default = -1, choices=MALOCCLUSION_CLASS_LIST)

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
        self.prediction_Angle_class_type_left = f'{malocclusion_predict["Left_class"]}'
        self.prediction_Angle_class_type_right = f'{malocclusion_predict["Right_class"]}'

        super().save(force_update=True)
