from django.urls import path
from django.views.generic.detail import DetailView

from .views import *
from .models import model_prediction_class

app_name = 'deep_learning_model_prediction_app'

urlpatterns = [
    path('', photo_list, name='photo_list'),
    path('detail/<int:pk>', DetailView.as_view(model=model_prediction_class,
                                               template_name='photo/detail.html'), name='photo_detail'),
    path('upload/', PhotoUploadView.as_view(), name='photo_upload'),
    path('delete/<int:pk>/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('update/<int:pk>/', PhotoUpdateView.as_view(), name='photo_update'),
]
