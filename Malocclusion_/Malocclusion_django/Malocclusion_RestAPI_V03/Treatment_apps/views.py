from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.filters import SearchFilter,OrderingFilter


from .models import Treatment
from .models import Patient
from .models import Organization
from .serializers import OrganizationSerializer
from .serializers import PatientSerializer
from .serializers import TreatmentSerializer


class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    # filter_backends = [SearchFilter,OrderingFilter]
    # search_fields = ['Organization_ID']
    # ordering_fields = ['patient_id']
    serializer_class = OrganizationSerializer
    name = 'organization-list'

class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    name = 'organization-detail'











class PatientList(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['Organization_ID']
    ordering_fields = ['patient_id']
    serializer_class = PatientSerializer
    name = 'patient-list'

class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    name = 'patient-detail'


class TreatmentList(generics.ListCreateAPIView):
    queryset = Treatment.objects.all()
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['patient_id']


    serializer_class = TreatmentSerializer
    name = 'treatment-list'




class TreatmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    name = 'treatment-detail'






class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'Organization RestAPI' : reverse(OrganizationList.name, request=request),
            'Patient RestAPI': reverse(PatientList.name, request=request),
            'Treatment TestAPI': reverse(TreatmentList.name, request=request),
            # information url 추가할것

            })

