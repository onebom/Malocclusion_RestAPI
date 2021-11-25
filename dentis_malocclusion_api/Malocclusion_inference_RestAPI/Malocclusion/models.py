import os
from django.utils import timezone
from django.db import models
from .mmmil.utils.postprocessing import malocclusion_result
import cv2 as cv
import random
import numpy as np
import string


def upload_to(instance, filename):
    n = 3
    rand_str = ""

    for i in range(n):
        rand_str += str(random.choice(string.ascii_uppercase))
    now = timezone.now()
    class_R = instance.Prediction_Angle_Class_R
    class_L = instance.Prediction_Angle_Class_L
    percent_R = instance.Prediction_Class_R_Percent
    percent_L = instance.Prediction_Class_L_Percent

    # return f"{now:%Y%m%d}/{rand_str}/R{class_R}_{percent_R}_L{class_L}_{percent_L}.jpg"

    return f"{now:%Y%m%d}/{rand_str}/{filename}"

class Malocclusion_Inference(models.Model):
    MALOCCLUSION_CLASS_LIST = [(-1, 'Not-defined'),(1, 'CLASS-1'), (2, 'CLASS-2'), (3, 'CLASS-3')]

    name = models.CharField(max_length=200, blank=False, default='')
    Malocclusion_Image = models.ImageField(upload_to = upload_to, blank=True)
    Prediction = models.CharField(max_length=46*5, default='None')
    Prediction_Angle_Class_R = models.IntegerField('Prediction Angle class type right',default = -1, choices=MALOCCLUSION_CLASS_LIST)
    Prediction_Angle_Class_L = models.IntegerField('Prediction Angle class type left',default = -1, choices=MALOCCLUSION_CLASS_LIST)
    Prediction_Class_R_Percent = models.CharField(max_length=46*5, default='None')
    Prediction_Class_L_Percent = models.CharField(max_length=46*5, default='None')


    class Meta:
        ordering = ('id',)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        malocclusion_predict = malocclusion_result(self.Malocclusion_Image.path)
        self.Prediction = f'{malocclusion_predict}'
        self.Prediction_Angle_Class_R = f'{malocclusion_predict["Right_class"]}'
        self.Prediction_Angle_Class_L = f'{malocclusion_predict["Left_class"]}'

        self.Prediction_Class_R_Percent = f'{np.max(malocclusion_predict["Right_onehot_predict"])}'
        self.Prediction_Class_L_Percent = f'{np.max(malocclusion_predict["Left_onehot_predict"])}'
        # print(self.Malocclusion_Image.path)
        # Malocclusion_img = cv.imread(self.Malocclusion_Image.path)
        dir_path = os.path.dirname(self.Malocclusion_Image.path)
        img_path = os.path.join(dir_path,f'R{self.Prediction_Angle_Class_R}_{self.Prediction_Class_R_Percent}_L{self.Prediction_Angle_Class_L}_{self.Prediction_Class_L_Percent}.jpg')
        os.renames(self.Malocclusion_Image.path,img_path)
        # cv.imwrite(img_path,Malocclusion_img)
        # print(self.Malocclusion_Image)
        # print(str(self.Malocclusion_Image).split('/'))
        string_path  = str(self.Malocclusion_Image).split('/')
        date = string_path[0]
        name = string_path[1]
        self.name = name
        image_path  = os.path.join(date,name,f'R{self.Prediction_Angle_Class_R}_{self.Prediction_Class_R_Percent}_L{self.Prediction_Angle_Class_L}_{self.Prediction_Class_L_Percent}.jpg')

        # print("#########################################")

        self.Malocclusion_Image = image_path
        super().save(force_update=True)

