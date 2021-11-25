from django.contrib import admin

# Register your models here.
from .models import model_prediction_class


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'created', 'updated']
    raw_id_fields = ['author']
    list_filter = ['created', 'updated', 'author']
    search_fields = ['text', 'created']
    ordering = ['-updated', '-created']


admin.site.register(model_prediction_class, PhotoAdmin)
