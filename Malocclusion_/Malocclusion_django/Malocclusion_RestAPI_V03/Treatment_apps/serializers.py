from rest_framework import serializers


from .models import Treatment
from .models import Patient
from .models import Organization


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    patients = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='patient-detail'
    )



    class Meta:
        model = Organization
        fields = ('url',
                  'Organization_id',
                  'Area_number',
                  'patients'
                  )


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    treatments = serializers.HyperlinkedRelatedField(

        many=True,
        read_only=True,
        view_name='treatment-detail')
    # organization_id = serializers.SlugRelatedField(queryset=Organization.objects.all(), slug_field='id')

    class Meta:
        model = Patient
        fields = ('url',
                  'Patient_id',
                  'Sex',
                  'Organization_ID',
                  'treatments'
                  )



class TreatmentSerializer(serializers.HyperlinkedModelSerializer):
    Patient_id = serializers.SlugRelatedField(queryset=Patient.objects.all(), slug_field='Patient_id')
    # Patient_id = serializers.HyperlinkedRelatedField(
    #
    #     many=True,
    #     read_only=True,
    #     view_name='patient-detail')



    class Meta:
        model = Treatment
        fields = ('url',
                  'Patient_id',
                  'State',
                  'Type',
                  'Treatment_id',
                  'Aangle_Class_L',
                  'Angle_Dis_L',
                  'Aangle_Class_R',
                  'Angle_Dis_R',
                  'Extraction_U',
                  'Extraction_D',
                  'Surgery_U',
                  'Surgery_D',
                  'Medical_image',
                  'Prediction',
                  'Prediction_Angle_Class_L',
                  'Prediction_Angle_Class_R',
                  )
        extra_kwargs = {'url': {'view_name': 'treatment-detail'}}

    # def save(self, *args, **kwargs):
    #     print(self)
    #     super().save(*args, **kwargs)
