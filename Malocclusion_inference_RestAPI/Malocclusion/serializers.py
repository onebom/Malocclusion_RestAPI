from rest_framework import serializers
from .models import Malocclusion_Inference

class MalocclusionInferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Malocclusion_Inference
        fields = ('url',
                  'id',
                  'name',
                  'Malocclusion_Image',
                  'Prediction',
                  'Prediction_Angle_Class_R',
                  'Prediction_Angle_Class_L',
                  'Prediction_Class_R_Percent',
                  'Prediction_Class_L_Percent',

                  )

    def save (self, *args, **kwargs):
        print(self)
        super().save(*args, **kwargs)
