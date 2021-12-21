
from django.contrib.auth.hashers import make_password
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
    code = models.CharField(max_length=5,  blank=True,
                            null=True, default=models.UUIDField)
    name = models.CharField(max_length=100, blank=False, null=False)
    crs = models.IntegerField(default=4326)
    wrap = models.BooleanField(default=False)
    geom = gismodels.MultiPolygonField(
        srid=4326, null=True, spatial_index=True, )

    class Meta:
        db_table = "country"


class Region(models.Model):
    code = models.CharField(max_length=50,  blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    geom = gismodels.MultiPolygonField(
        srid=4326, null=True, spatial_index=True, )

    class Meta:
        db_table = "region"


class City(models.Model):
    code = models.IntegerField(blank=False, null=False)
    region_name = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    geom = gismodels.PointField(srid=4326, spatial_index=True, null=True)
    name_de = models.CharField(
        max_length=100, blank=True, null=True, default="")
    name_en = models.CharField(
        max_length=100, blank=True, null=True, default="")
    name_es = models.CharField(
        max_length=100, blank=True, null=True, default="")
    name_fr = models.CharField(
        max_length=100, blank=True, null=True, default="")
    name_pt = models.CharField(
        max_length=100, blank=True, null=True, default="")
    name_ru = models.CharField(
        max_length=100, blank=True, null=True, default="")
    name_zh = models.CharField(
        max_length=100, blank=True, null=True, default="")

    class Meta:
        db_table = "cities"


class Aoi(models.Model):
    name = models.CharField(max_length=100, default=None)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, null=True)
    region = models.ForeignKey(
        Region, on_delete=models.DO_NOTHING, null=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True)
    buffer_size = models.FloatField(default=0.0)
    geom = gismodels.PolygonField(
        srid=4326, spatial_index=True, null=True)

    date_created = models.DateTimeField(default=now)

    class Meta:
        db_table = "area_of_interest"


class Settings(models.Model):
    can_email_result = models.BooleanField(
        default=True, null=True, blank=True)
    in_mail_list = models.BooleanField(default=False, null=True, blank=True)
    update_frequency_milliseconds = models.IntegerField(
        null=True, blank=True, default=10000)
    buffer_checked = models.BooleanField(null=True, default=True, blank=True)
    buffer_size = models.FloatField(null=True, default=10.0, blank=True)
    data_age_limit = models.IntegerField(null=True, blank=True, default=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

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
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "execution_script"


class Script(models.Model):
    execution_script = models.ForeignKey(
        ExecutionScript, on_delete=models.DO_NOTHING)
    parametrization_dialogue = models.TextField(default=None)

    class Meta:
        db_table = "script"


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

    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "algorithm"


class Feedback(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, default=None)
    title = models.CharField(max_length=255, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "feedbacks"


class Role(models.Model):
    code = models.CharField(max_length=50, default="", null=True, blank=True)
    value = models.CharField(max_length=100, default="", null=True, blank=True)
    value = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "account_roles"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, null=True, blank=True)
    organization = models.CharField(max_length=200, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)
    photo = models.CharField(null=True, blank=True, default="", max_length=200)

    role = models.ForeignKey(Role, default=1, on_delete=models.CASCADE)
    uid = models.CharField(max_length=200, default="", null=True, blank="")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
