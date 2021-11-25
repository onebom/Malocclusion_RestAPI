from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Malocclusion_Inference

from .serializers import MalocclusionInferenceSerializer


class MalocclusionInferenceList(generics.ListCreateAPIView):
    queryset = Malocclusion_Inference.objects.all()
    serializer_class = MalocclusionInferenceSerializer
    name = 'malocclusion_inference-list'

class MalocclusionInferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Malocclusion_Inference.objects.all()
    serializer_class = MalocclusionInferenceSerializer
    name = 'malocclusion_inference-detail'



class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'Malocclusion Inference RestAPI': reverse(MalocclusionInferenceList.name, request=request),
            # 'landmark ': 'http://127.0.0.1:8000/landmark/',
            })

