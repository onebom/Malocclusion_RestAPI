from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.filters import SearchFilter,OrderingFilter


from .models import Treatment

from .serializers import TreatmentSerializer



class TreatmentList(generics.ListCreateAPIView):
    queryset = Treatment.objects.all()
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']


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
            'Treatment TestAPI': reverse(TreatmentList.name, request=request),
            # information url 추가할것
            })

