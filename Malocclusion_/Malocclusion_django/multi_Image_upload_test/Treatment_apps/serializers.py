from rest_framework import serializers


from .models import Treatment




class TreatmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Treatment
        fields = ('url',

                  'id',

                  'Medical_image',
                  'Medical_image1',
                  'Medical_image2',

                  'prediction_result',
                  )
        extra_kwargs = {'url': {'view_name': 'treatment-detail'}}

