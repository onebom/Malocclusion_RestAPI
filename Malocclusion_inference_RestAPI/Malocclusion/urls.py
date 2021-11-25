from django.urls import path, include
from . import views

urlpatterns = [

        path('MalocclussionInference/v01/', views.MalocclusionInferenceList.as_view(),
            name = views.MalocclusionInferenceList.name),

        path('MalocclussionInference/v01/<int:pk>', views.MalocclusionInferenceDetail.as_view(),
            name = views.MalocclusionInferenceDetail.name),

        path('',views.ApiRoot.as_view(), name = views.ApiRoot.name),

]




from django.conf.urls.static import static
from django.conf import settings

#-----------------------------
# service의 경우, 변경이 필요한 부분임.
# TODO 2021.06.14 dsaint31
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
