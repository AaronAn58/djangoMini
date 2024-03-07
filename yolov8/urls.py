from django.urls import path
from .views import video_list, upload_video, analyze_video, delete_video, check_report, show_report, download_report

app_name = "yolov8"
urlpatterns = [
    path('list/', video_list, name='video_list'),
    path('upload/', upload_video, name='upload_video'),
    path('analyze/', analyze_video, name='analyze_video'),
    path('delete_video/<int:video_id>/', delete_video, name='delete_video'),
    path('check_report/<int:video_id>/', check_report, name='check_report'),
    path('show_report/<int:video_id>/', show_report, name='show_report'),
    path('download_report/<int:video_id>/', download_report, name='download_report'),
]
