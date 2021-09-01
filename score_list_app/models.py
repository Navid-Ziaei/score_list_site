from django.db import models

from django.contrib.auth.models import User
from .validators import validate_file_extension


# Create your models here.
class ToDo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    date_completed = models.DateField(null=True, blank=True)
    important = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UploadFile(models.Model):
    upload = models.FileField(upload_to= "score_list_app/static/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ScoreList(models.Model):
    score_project1 = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

