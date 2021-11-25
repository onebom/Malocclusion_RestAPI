from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import DeepLearningModelInference

from .serializers import DeepLearningModelInferenceSerializer

class DeepLearningModelInferenceList(generics.ListCreateAPIView):
    queryset = DeepLearningModelInference.objects.all()
    serializer_class = DeepLearningModelInferenceSerializer
    name = 'Malocclusion_Model_Inference-list'

class DeepLearningModelInferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeepLearningModelInference.objects.all()
    serializer_class = DeepLearningModelInferenceSerializer
    name = 'Malocclusion_Model_Inference-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'Malocclusion_Model_Inference': reverse(DeepLearningModelInferenceList.name, request=request),
            })

