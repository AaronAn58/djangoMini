# Create your models here.
from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title


class Report(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    total = models.IntegerField(null=False, default=0, blank=False)
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.video.title
