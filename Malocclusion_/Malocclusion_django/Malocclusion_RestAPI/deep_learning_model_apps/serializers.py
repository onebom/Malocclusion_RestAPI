from rest_framework import serializers


from .models import DeepLearningModelInference

class DeepLearningModelInferenceSerializer(serializers.ModelSerializer):

    Medical_image = serializers.ImageField(use_url=True)

    class Meta:
        model  = DeepLearningModelInference
        fields = ('url','id', 'name', 'Medical_image',
                  'prediction_result')
        extra_kwargs = {'url': {'view_name':  'Malocclusion_Model_Inference-detail'}}

    def save (self, *args, **kwargs):
        print(self)
        super().save(*args, **kwargs)

