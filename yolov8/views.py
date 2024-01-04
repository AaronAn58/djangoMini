import multiprocessing
from pathlib import Path

import cv2
import thread6
from django.shortcuts import render, redirect
from ultralytics import YOLO

from .forms import VideoForm
from .models import Video


def video_list(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video_list')
    else:
        form = VideoForm()
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos, 'form': form})


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'video_list.html', {'form': form})


def analyze_video(request):
    params = request.GET
    # model_pt = params.get('model')
    model_pt = "best.pt"
    video_name = params.get('video')
    video_name = video_name.split('/')[-1]
    video_analysis_mul_process(model_pt, video_name)
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})


@thread6.threaded(False)
def video_analysis_mul_process(model_pt, video_name):
    lock = multiprocessing.Semaphore(2)
    p = multiprocessing.Process(target=video_analysis,
                                args=(lock, model_pt, video_name))
    p.run()


def video_analysis(lock, model_pt, video_name):
    lock.acquire()
    base_dir = Path(__file__).resolve().parent
    model_name = str(base_dir) + "\\config\\" + model_pt
    video = str(base_dir) + "\\config\\videos\\" + video_name
    model = YOLO(model_name)
    cap = cv2.VideoCapture(video)
    while True:
        ret, im2 = cap.read()
        if not ret:
            cv2.waitKey(0)
            break
        im2 = cv2.resize(im2, (0, 0), fx=0.5, fy=0.5)
        model.predict(source=im2, save=False, save_txt=False, show=True)  # save predictions as labels
    lock.release()


def upload_report(video_name, report):
    pass
