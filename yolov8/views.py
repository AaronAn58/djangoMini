import multiprocessing

import thread6
from django.shortcuts import render, redirect
from ultralytics import YOLO

from .forms import VideoForm
from .models import Video
import cv2


def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})


def analyze_video(request):



@thread6.threaded(False)
def video_analysis_mul_process():
    lock = multiprocessing.Semaphore(2)
    p = multiprocessing.Process(target=video_analysis,
                                args=lock)
    p.run()


def video_analysis():
    model = YOLO("best.pt")
    cap = cv2.VideoCapture("videos/0.mp4")
    while True:
        ret, im2 = cap.read()
        if ret == False:
            cv2.waitKey(0)
            break
        im2 = cv2.resize(im2, (0, 0), fx=0.5, fy=0.5)
        results = model.predict(source=im2, save=False, save_txt=False, show=True)  # save predictions as labels
