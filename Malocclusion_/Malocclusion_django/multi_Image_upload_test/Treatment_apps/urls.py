from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [


    url(r'^v01/treatments/$',
        views.TreatmentList.as_view(),
        name=views.TreatmentList.name),

    url(r'^v01/treatment/(?P<pk>[0-9]+)/$',
        views.TreatmentDetail.as_view(),
        name=views.TreatmentDetail.name),

    url(r'^$',
        views.ApiRoot.as_view(),
        name=views.ApiRoot.name),
]





from django.conf.urls.static import static
from django.conf import settings
#-----------------------------
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
