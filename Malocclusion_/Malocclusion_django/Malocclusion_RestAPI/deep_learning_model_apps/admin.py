from django.contrib import admin
from .models import DeepLearningModelInference
# Register your models here.

@admin.register(DeepLearningModelInference)
class DeepLearningModelInferenceAdmin(admin.ModelAdmin):
  pass
