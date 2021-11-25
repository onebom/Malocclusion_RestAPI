from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from .mmmil.utils.postprocessing import malocclusion_result
import cv2 as cv


def upload_to(instance, filename):
    return f"{filename}"


class model_prediction_class(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_photos')

    name = models.CharField(max_length=200, blank=False, default='')
    photo = models.ImageField(upload_to=upload_to, blank=True)
    Description_R = models.CharField(max_length=46 * 5, default='None')

    # ip = models.GenericIPAddressField(null=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-updated']

    def __str__(self):
        print(self.photo.path)
        img = cv.imread(self.photo.path)
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self):
        print(self.photo.path)
        img = cv.imread(self.photo.path)
        return reverse('deep_learning_model_prediction_app:photo_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        malocclusion_predict = malocclusion_result(self.photo.path)
        self.Description_R = f'{malocclusion_predict}'
        super().save(force_update=True)

