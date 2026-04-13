from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('/',views.hello ,name=""),
    # path('/',views.download_video_info ,name=""),
    path('vdo/',views.download_video_info1 ,name="video_request"),
    # path('request/',views.download_video_info ,name="video_request"),
    # path('',views.aiRequest ,name="ai_request"),
    path('request/',views.aiRequest ,name="ai_request"),
    # path('v/',views.download_video_api ,name="video_request"),
    path('info/',views.download_video_info ,name="video_request"),
    path('download/',views.download_video_file ,name="video_download"),
]
