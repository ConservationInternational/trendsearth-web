import enum
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils import tree
from django.utils.timezone import now

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


class Result(models.Model):
    code = models.CharField(max_length=20)
    value = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        db_table = "job_results"


class RemoteScript(models.Model):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=150)
    description = models.TextField()
    status = models.ForeignKey(ScriptStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    class Meta:
        db_table = "remote_scripts"


class LocalContext(models.Model):
    base_dir = models.CharField(max_length=150)
    aoi = models.ForeignKey(Aoi, on_delete=models.CASCADE)

    class Meta:
        db_table = "local_contents"


class Parameters(models.Model):
    name = models.CharField(max_length=150)
    params = models.JSONField()

    class Meta:
        db_table = "parameters"


class Notes(models.Model):
    note = models.TextField(blank=True, null=True)
    local_context = models.ForeignKey(
        LocalContext, on_delete=models.CASCADE)
    parameter = models.ForeignKey(
        Parameters, on_delete=models.CASCADE, default=None)

    class Meta:
        db_table = "notes"


class Band(models.Model):
    metadata = models.JSONField()
    name = models.CharField(max_length=150)
    no_data_value = models.FloatField(default=-32768.0)
    activated = models.BooleanField(default=True)
    add_to_map = models.BooleanField(default=True)

    class Meta:
        db_table = "bands"


class Url(models.Model):
    url = models.CharField(max_length=150)
    md5_hash = models.CharField(max_length=150)

    class Meta:
        db_table = "urls"


class CloudResults(models.Model):
    name = models.CharField(max_length=150)
    bands = models.ManyToManyField(Band)
    urls = models.ManyToManyField(Url)
    data_path = models.CharField(max_length=150)
    other_paths = ArrayField(ArrayField(models.CharField(max_length=200)))
    jobresult_type = models.ForeignKey(
        Result, default=1, on_delete=models.CASCADE)

    class Meta:
        db_table = "cloud_results"


class TimeSeriesTableResult(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    table = ArrayField(ArrayField(models.JSONField()))
    jobresult_type = models.ForeignKey(
        Result, on_delete=models.CASCADE, default=3)

    class Meta:
        db_table = "timeseries_tbl_results"


class LocalResults(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    bands = models.ManyToManyField(Band)
    data_path = models.CharField(max_length=200)
    other_paths = ArrayField(ArrayField(models.CharField(max_length=200)))
    jobresult_type = models.ForeignKey(
        Result, on_delete=models.CASCADE, default=2)

    class Meta:
        db_table = "local_results"


class Job(models.Model):
    params = models.ForeignKey(Parameters, on_delete=models.CASCADE)
    progress = models.IntegerField()
    jobcloudresult = models.ForeignKey(
        CloudResults, on_delete=models.CASCADE)
    jobLocalResult = models.ForeignKey(
        LocalResults, on_delete=models.CASCADE)
    timeseriestableresult = models.ForeignKey(
        TimeSeriesTableResult, on_delete=models.CASCADE)
    script = models.ForeignKey(ExecutionScript, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "jobs"
