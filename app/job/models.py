import enum
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils import tree
from django.utils.timezone import now

from account.models import Aoi, Script


class Status(models.Model):
    code = models.CharField(max_length=20)
    value = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        db_table = "job_status"


class Job(models.Model):
    progress = models.IntegerField()
    script = models.ForeignKey(
        Script, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True, default=now)
    end_date = models.DateTimeField(null=True, blank=True)
    uid = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    results = models.JSONField({}, null=True, blank=True)
    task_name = models.CharField(max_length=250, default="")
    task_notes = models.TextField(default="")

    class Meta:
        db_table = "jobs"
        ordering = ('-start_date',)


class Layer(models.Model):
    name = models.CharField(max_length=200)
    layername = models.CharField(max_length=100, default="")
    url = models.CharField(max_length=200)
    workspace = models.CharField(max_length=50, default="ldmp")
    created_at = models.DateTimeField(auto_now_add=True)
    is_result = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.OneToOneField(Job, on_delete=models.CASCADE,
                               null=True)
    is_base = models.BooleanField(default=False)

    class Meta:
        db_table = "layers"
