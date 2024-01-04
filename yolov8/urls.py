from django.urls import path
from .views import video_list, upload_video, analyze_video

urlpatterns = [
    path('list/', video_list, name='video_list'),
    path('upload/', upload_video, name='upload_video'),
    path('analyze/', analyze_video, name='analyze_video'),
]
