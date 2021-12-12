import enum
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils import tree
from django.utils.timezone import now
from requests.sessions import default_headers

from account.models import Aoi, ExecutionScript
# Create your models here.


class SortField(enum.Enum):
    NAME = 'name'
    DATE = 'date'
    ALGORITHM = 'algorithm'
    STATUS = 'status'


class ScriptStatus(models.Model):
    code = models.CharField(max_length=20)
    value = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        db_table = "script_status"


class Status(models.Model):
    code = models.CharField(max_length=20)
    value = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        db_table = "job_status"


class Job(models.Model):
    progress = models.IntegerField()
    script = models.ForeignKey(
        ExecutionScript, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True, default=now)
    end_date = models.DateTimeField(null=True, blank=True)
    uid = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    results = models.JSONField({}, null=True, blank=True)

    class Meta:
        db_table = "jobs"
