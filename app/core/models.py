# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class AggregationInputClass(models.Model):
    code = models.CharField(max_length=20, null=False, blank=False)
    color = models.CharField(max_length=20, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    name_short = models.CharField(max_length=50, blank=True, null=True)
    name_long = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = "aggregation_input_class"


class AggregationOutputClass(models.Model):
    code = models.CharField(max_length=20, null=False, blank=False)
    color = models.CharField(max_length=20, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    name_short = models.CharField(max_length=50, blank=True, null=True)
    name_long = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = "aggregation_output_class"


class UserAggregationClass(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    inputclass = models.ForeignKey(
        AggregationInputClass, null=False, blank=False,
        on_delete=models.CASCADE)
    outputclass = models.ForeignKey(
        AggregationOutputClass, null=False, blank=False,
        on_delete=models.CASCADE)

    class Meta:
        db_table = "user_aggregation_class"
