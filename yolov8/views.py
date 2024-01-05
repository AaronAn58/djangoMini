import multiprocessing
import os
from pathlib import Path

import cv2
import thread6
from PIL import Image
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from ultralytics import YOLO

from .forms import VideoForm
from .models import Video

base_dir = Path(__file__).resolve().parent


def video_list(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('yolov8:video_list')
    else:
        form = VideoForm()
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos, 'form': form})


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('yolov8:video_list')
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
    model_name = str(base_dir) + "\\config\\" + model_pt
    video = str(base_dir) + "\\config\\videos\\" + video_name
    model = YOLO(model_name)
    cap = cv2.VideoCapture(video)
    results = None
    while True:
        ret, im2 = cap.read()
        if not ret:
            # cv2.waitKey(0)
            break
        im2 = cv2.resize(im2, (0, 0), fx=0.5, fy=0.5)
        results = model.predict(source=im2, save=True, save_txt=True, show=True, save_crop=True, )  # save predictions as labelsre
    results.plot()
    # model.export(format="onnx")
    lock.release()


def upload_report(video_name, report):
    pass


def delete_video(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, pk=video_id)
        video_file = str(base_dir) + "\\config\\" + str(video.file.name)
        delete_file(video_file)
        video.delete()
        return JsonResponse({'message': 'Video deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except OSError as e:
        print(f"Error deleting file '{file_path}': {e}")
