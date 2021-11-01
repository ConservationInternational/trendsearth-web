
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import empty
from django.utils.timezone import now


class Continent(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    geom = gismodels.MultiPolygonField(
        srid=4326, spatial_index=True, null=True)

    class Meta:
        db_table = "continent"


class Country(models.Model):
    code = models.CharField(max_length=5,  blank=True, null=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    continent = models.ForeignKey(Continent, on_delete=models.DO_NOTHING)
    geom = gismodels.MultiPolygonField(
        srid=4326, spatial_index=True, null=True)

    class Meta:
        db_table = "country"


class Region(models.Model):
    code = models.CharField(max_length=5,  blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    geom = gismodels.MultiPolygonField(
        srid=4326, spatial_index=True, null=True)

    class Meta:
        db_table = "region"


class Aoi(models.Model):
    name = models.CharField(max_length=100, default=None)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    geom = gismodels.MultiPolygonField(
        srid=4326, spatial_index=True, null=True)

    date_created = models.DateTimeField(default=now)

    class Meta:
        db_table = "area_of_interest"


class Settings(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        db_table = "settings"


class AlgorithmNodeType(models.Model):
    code = models.CharField(max_length=5,  blank=True, null=True)
    value = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        db_table = "algorigthm_nodetype"


class AlgorithmRunMode(models.Model):
    code = models.CharField(max_length=10,  blank=True, null=True)
    value = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        db_table = "algorithm_runmode"


class ExecutionScript(models.Model):
    uid = models.CharField(max_length=150, null=True, blank=True)
    name = models.CharField(max_length=150,  blank=True, null=True)
    run_mode = models.ForeignKey(
        AlgorithmRunMode, on_delete=models.DO_NOTHING, default=1)
    version = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    name_readable = models.CharField(max_length=150, null=True, blank=True)
    additional_configuration = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "execution_script"


class Script(models.Model):
    execution_script = models.ForeignKey(
        ExecutionScript, on_delete=models.DO_NOTHING)
    parametrization_dialogue = models.TextField(default=None)

    class Meta:
        db_table = "script"


# class AlgorithmGroup(models.Model):
#     name = models.CharField(max_length=150,  blank=True, null=True)
#     name_details = models.TextField(blank=True, null=True)
#     groups = models.ManyToManyField('self', blank=True)
#     parent = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING)
#     item_type = models.ForeignKey(
#         AlgorithmNodeType, on_delete=models.DO_NOTHING, default=1)

#     class Meta:
#         db_table = "algorithm_group"


class Algorithm(models.Model):
    uid = models.CharField(max_length=150, null=True, blank=True)
    name = models.CharField(max_length=150,  blank=True, null=True)
    name_details = models.TextField(default=None,  blank=True, null=True)
    brief_description = models.TextField(default=None,  blank=True, null=True)
    description = models.TextField(default=None,  blank=True, null=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True,  on_delete=models.DO_NOTHING)
    item_type = models.ForeignKey(
        AlgorithmNodeType, on_delete=models.DO_NOTHING, default=2)
    scripts = models.ManyToManyField(Script)

    class Meta:
        db_table = "algorithm"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    organization = models.CharField(max_length=200, null=False, blank=False)
    deleted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
