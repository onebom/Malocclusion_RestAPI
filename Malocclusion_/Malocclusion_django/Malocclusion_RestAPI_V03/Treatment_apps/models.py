import os
from django.utils import timezone
from django.db import models
from .mmmil.utils.postprocessing import malocclusion_result
import cv2 as cv
from django.contrib.auth.models import User # 계정 관련 모델.
import pandas as pd



import threading

ds_lock = threading.Lock()


'''
저장 경로 함수 설정
'''
def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    patient_id = instance.Patient_id.Patient_id
    tx_phase = instance.State
    if tx_phase == 0:
        tx_phase = 'A'
    elif tx_phase == 1 :
        tx_phase = 'B'
    else :
        tx_phase = 'C'



    return f"{now:%Y%m%d}/QH{patient_id:04d}_{tx_phase}.jpg"

'''
Organization DB 선언 부분
'''


class Organization(models.Model):
    Organization_id = models.BigAutoField(primary_key = True)
    # owner  = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    # 지역.
    code_list = [('002', '서울'), ('031', '경기도'), ('032', '인천'), ('033', '강원도'), ('041', '충청남도'), ('042', '대전'),
                 ('043', '충청북도'),
                 ('044', '세종'), ('051', '부산'), ('052', '울산'), ('053', '대구'), ('054', '경상북도'), ('055', '경상남도'),
                 ('061', '전라남도'),
                 ('062', '광주'), ('063', '전라북도'), ('064', '제주')]
    Area_number = models.CharField('AREA', max_length=3, blank=True, null=True, choices=code_list)

    class Meta:
        ordering = ('Organization_id',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


''' 
Patient DB 선언 부분
'''
class Patient(models.Model):
    Patient_id               = models.BigAutoField(primary_key=True)


    Sex = models.IntegerField('Sex', default=0,
                               choices=[(0, 'Male'),
                                        (1, 'Female'),
                                        ])

    Organization_ID = models.ForeignKey(
        Organization,
        related_name='patients',
        on_delete=models.CASCADE)



    class Meta:
        ordering = ('Patient_id',)

    def save(self, *args, **kwargs):
        # self.patient_id_str = f'KO{self.Organization_ID:04d}{self.patient_id:04d}'

        super().save(*args, **kwargs)
        #
        # self.patient_id_str = f'KO{self.Organization_ID:04d}{self.patient_id:04d}'
        #
        # super().save(force_update=True)

'''
Treatment DB 선언 부분
'''


class Treatment(models.Model):
    CLR_EXT_LIST = [(0, 'Clear Aligner'), (1, 'Extraction'), (-1, 'Not-defined')]
    MALOCCLUSION_CLASS_LIST = [(1, 'CLASS-1'), (2, 'CLASS-2'), (3, 'CLASS-3'), (-1, 'Not-defined')]
    extraction = [(0, 'non extraction'), (1, 'extraction on upper')]
    surgery = [(0,'non Surgery'),(1,'Surgery')]

    Patient_id = models.ForeignKey(
        Patient,
        related_name='treatments',
        on_delete=models.CASCADE)

    Treatment_id = models.BigAutoField(primary_key=True)

    State = models.IntegerField('Treatment state', default=0,
                               help_text='치료전:0 / 치료후:1 / 미정:2',
                               choices=[(0, 'Pre'),
                                        (1, 'Post'),
                                        (2, 'Not defined')
                                        ])  # 치료후 데이터인지.

    Type = models.IntegerField('Treatment Type',default=-1,choices=CLR_EXT_LIST)


    Aangle_Class_L = models.IntegerField('Angle class type left',default = -1, choices=MALOCCLUSION_CLASS_LIST)
    Angle_Dis_L = models.FloatField('Angle distance left(mm)',default = 0)
    Aangle_Class_R = models.IntegerField('Angle class type right', default = -1,choices=MALOCCLUSION_CLASS_LIST)
    Angle_Dis_R= models.FloatField('Angle distance right(mm)',default=0)
    Extraction_U = models.IntegerField('Extraction Upper', default=0, choices=extraction)
    Extraction_D = models.IntegerField('Extraction Lower', default=0, choices=extraction)
    Surgery_U = models.IntegerField('Surgery Upper', default=0, choices=surgery)
    Surgery_D = models.IntegerField('Surgery Lower', default=0, choices=surgery)

    Medical_image = models.ImageField(upload_to = upload_to, blank=True)


    Prediction = models.CharField(max_length=46*5, default='None')
    Prediction_Angle_Class_L = models.IntegerField('Prediction Angle class type left',default = -1, choices=MALOCCLUSION_CLASS_LIST)
    Prediction_Angle_Class_R = models.IntegerField('Prediction Angle class type right',default = -1, choices=MALOCCLUSION_CLASS_LIST)

    # ip = models.GenericIPAddressField(null=True, editable=False)

    class Meta:
        ordering = ('Treatment_id',)

    #@async_to_sync
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ds_lock.acquire()
        malocclusion_predict = malocclusion_result(self.Medical_image.path)
        print(self.Medical_image.path)
        # print(os.pardir(self.Medical_image.path))



        ds_lock.release()
        self.Prediction = f'{malocclusion_predict}'
        self.Prediction_Angle_Class_L = f'{malocclusion_predict["Left_class"]}'
        self.Prediction_Angle_Class_R = f'{malocclusion_predict["Right_class"]}'
        csv_path = os.path.join(os.path.dirname(self.Medical_image.path),'label.csv')
        print(self.Patient_id.Patient_id)

        if os.path.isfile(csv_path) == False:
            df1 = pd.DataFrame({'patient_id': [],
                                'tx_phase': [],
                                'angle_class_r': [],
                                'angle_class_l': [],
                                'distance(r)': [],
                                'distance(l)': []})

            tx_phase = self.State
            if tx_phase == 0:
                tx_phase = 'Pre-Tx'
            elif tx_phase == 1:
                tx_phase = 'Post-Tx'
            else:
                tx_phase = 'not-defined'


            df2 = pd.DataFrame({'patient_id': [f'QH{int(self.Patient_id.Patient_id):04d}'],
                                'tx_phase': [tx_phase],
                                'angle_class_r': [self.Prediction_Angle_Class_R],
                                'angle_class_l': [self.Prediction_Angle_Class_L ],
                                'distance(r)': [self.Angle_Dis_R],
                                'distance(l)': [self.Angle_Dis_L]})

            result = df1.append(df2)
            result.to_csv(csv_path,index=False)









        else :
            df1 = pd.read_csv(csv_path)
            tx_phase = self.State
            if tx_phase == 0:
                tx_phase = 'Pre-Tx'
            elif tx_phase == 1:
                tx_phase = 'Post-Tx'
            else:
                tx_phase = 'not-defined'


            df2 = pd.DataFrame({'patient_id': [f'QH{int(self.Patient_id.Patient_id):04d}'],
                                'tx_phase': [tx_phase],
                                'angle_class_r': [self.Prediction_Angle_Class_R],
                                'angle_class_l': [self.Prediction_Angle_Class_L ],
                                'distance(r)': [self.Angle_Dis_R],
                                'distance(l)': [self.Angle_Dis_L]})

            result = df1.append( df2)
            result.to_csv(csv_path,index=False)
        super().save(force_update=True)
