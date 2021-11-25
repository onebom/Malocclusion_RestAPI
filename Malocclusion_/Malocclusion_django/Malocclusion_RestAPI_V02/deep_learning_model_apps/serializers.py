from rest_framework import serializers


from .models import DeepLearningModelInference

class DeepLearningModelInferenceSerializer(serializers.ModelSerializer):

    Medical_image = serializers.ImageField(use_url=True)

    class Meta:
        model  = DeepLearningModelInference
        fields = ('url',
                  'treatment_id',
                  'id',
                  'treatment_state',
                  'Treatment_Type',
                  'Angle_class_type_left',
                  'Angle_class_dist_left',
                  'Angle_class_type_right',
                  'Angle_class_dist_right',
                  'extraction_upper',
                  'extraction_lower',
                  'Surgery_upper',
                  'Surgery_lower',
                  'Medical_image',
                  'prediction_result',
                  'prediction_Angle_class_type_left',
                  'prediction_Angle_class_type_right',
                  )
        extra_kwargs = {'url': {'view_name':  'Malocclusion_Model_Inference-detail'}}

    def save (self, *args, **kwargs):
        print(self)
        super().save(*args, **kwargs)

