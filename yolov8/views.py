import json
import multiprocessing
import os
import ast
from pathlib import Path
from collections import Counter

import cv2
import thread6
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from ultralytics import YOLO

from .forms import VideoForm, ReportForm
from .models import Video, Report

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
    video_id = params.get('id')
    video_name = video_name.split('/')[-1]
    video_analysis_mul_process(model_pt, video_name, video_id)
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})


@thread6.threaded(False)
def video_analysis_mul_process(model_pt, video_name, video_id):
    lock = multiprocessing.Semaphore(2)
    p = multiprocessing.Process(target=video_analysis,
                                args=(lock, model_pt, video_name, video_id))
    p.run()


def video_analysis(lock, model_pt, video_name, video_id):
    lock.acquire()
    model_name = str(base_dir) + "\\config\\" + model_pt
    video = str(base_dir) + "\\config\\videos\\" + video_name
    model = YOLO(model_name)
    cap = cv2.VideoCapture(video)
    results = []
    total = 0
    while True:
        total += 1
        ret, im2 = cap.read()
        if not ret:
            # cv2.waitKey(0)
            break
        im2 = cv2.resize(im2, (0, 0), fx=0.5, fy=0.5)
        results.append(model.predict(source=im2, save=True, save_txt=True, show=True,
                                     save_crop=True, ))  # save predictions as labelsre
    counter = analyze_result(results)
    video_obj = Video.objects.get(id=int(video_id))
    report = Report(video=video_obj,
                    report=counter,
                    total=total)
    report.save()
    lock.release()


def analyze_result(results):
    filter_type = list(results[0][0].names.keys())
    all_results = []
    for result in results:
        if result[0].boxes.cls.numel() > 0:
            all_results.extend(result[0].boxes.cls.tolist())
    all_results = [int(x) for x in all_results]
    counter = Counter(all_results)
    result_dict = {results[0][0].names[key]: counter[key] for key in filter_type}
    return result_dict


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


def check_report(request, video_id):
    # 根据 video_id 查询对应的视频
    video = get_object_or_404(Video, id=int(video_id))

    # 根据视频查询报告
    report = Report.objects.filter(video=video).first()

    # 如果报告存在，则返回 True；否则返回 False
    has_report = True if report else False

    # 返回 JSON 响应
    return JsonResponse({'has_report': has_report})


def show_report(request, video_id):
    # 根据 video_id 查询对应的视频
    video = get_object_or_404(Video, id=int(video_id))

    # 根据视频查询报告
    report_obj = Report.objects.filter(video=video).first()
    total = report_obj.total
    report_result = json.loads(json.dumps(report_obj.report))
    report_result = ast.literal_eval(report_result)
    report_result["total"] = total

    return JsonResponse({'report': report_result})
