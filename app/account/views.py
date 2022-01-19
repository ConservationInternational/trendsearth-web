import os
import json
from datetime import (
    datetime,
    timedelta
)
from tkinter.messagebox import NO
from django.db import connection
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse
)
from django.contrib.gis.geos import Point, Polygon
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.hashers import make_password
from django.template import loader
from django.contrib.auth import (
    login,
    authenticate,
    logout
)
from django.views.generic.edit import FormView
from django.contrib import messages
from django.conf import settings
from django.db import connection

# from osgeo import ogr

from account import models
from job.models import (Job, Status)
from . import forms

from utils.api import (Api)
from utils.util import dictfetchall


def signout(request):
    """Logout an active session

    Args:
        request (request): http request

    Returns:
        HttpResponse: If session is active, log out and redirect
        the view to home page
    """
    logout(request)
    if "bearer_token" in request.session:
        del request.session['bearer_token']

    return HttpResponseRedirect(reverse_lazy('home'))


def home_view(request):
    """Load logged in user profile view
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('dashboard'))

    template = loader.get_template('account/index.html')
    context = {
        'user': request.user
    }
    return HttpResponse(template.render(context, request))


class LoginView(FormView):
    """Renders to the login view

    Returns:
        HTTP Response: HTML content with the login view
    """

    form_class = forms.LoginForm
    success_url = reverse_lazy('dashboard')
    template_name = 'account/login-page.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        api = Api(email=credentials['email'],
                  password=credentials['password'])
        self.request.session['bearer_token'] = api.token
        api_user = api.get_user()
        if api_user is None:
            messages.add_message(self.request, messages.ERROR,
                                 'User with these credentials not available!')
            return HttpResponseRedirect(reverse_lazy('login'))
        else:
            user, created = User.objects.update_or_create(
                email=credentials['email'],
                defaults={
                    'is_staff': False,
                    'is_superuser': api_user["role"] != 'USER',
                    'is_active': True,
                    'first_name': api_user["name"].split(" ")[0],
                    'last_name': api_user["name"].split(" ")[1],
                    'email': api_user["email"],
                    'username': api_user["email"],
                    'password': make_password(credentials['password'])
                })

            try:
                country = models.Country.objects.get(
                    name=api_user.get('country'))

                role = models.Role.objects.get(
                    code=api_user.get('role', 'USER'))
                profile, created = models.Profile.objects.update_or_create(
                    user=user,
                    defaults={
                        "country_id": country.id,
                        "organization": api_user.get('institution', ''),
                        "uid": api_user.get('id', ''),
                        "role_id": role.id
                    }
                )
                if profile.region is None:
                    region = models.Region.objects.filter(
                        country=country).first()
                    profile.region = region
                    profile.save(update_fields=["region"])

            except Exception as e:
                print(e)

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])
        if user is not None and not user.profile.deleted:
            login(self.request, user)

            """if user.is_superuser:
                with connection.cursor() as cursor:
                    querystr = "SELECT id, code FROM country"
                    cursor.execute(querystr)
                    records = dictfetchall(cursor)
                    for record in records:
                        filepath = os.path.dirname(os.path.abspath(__file__)) + "/configs/admin_bounds/admin_bounds_polys_{country}.json/admin_bounds_polys_{country}.json".format(
                            country=record.get("code"))
                        country = json.load(open(filepath))
                        querystr = "UPDATE country SET geom = ST_GeomFromGeoJSON('{}') WHERE id={}".format(
                            json.dumps(country.get("geojson").get("geometry")), record.get("id"))
                        cursor.execute(querystr)
                        print(querystr)
                        for key, value in country.get("admin1").items():
                            querystr = "UPDATE region SET geom = ST_GeomFromGeoJSON('{}') WHERE code='{}' AND country_id={}".format(
                                json.dumps(value.get("geojson").get("geometry")), key, record.get("id"))
                            cursor.execute(querystr)"""
            today = datetime.now()
            if models.Settings.objects.filter(user=user).count() == 0:
                models.Settings.objects.update_or_create(
                    in_mail_list=False, user=user)
            age_limits = models.Settings.objects.get(
                user=user).data_age_limit
            age_limits = 150
            startdate = today - timedelta(days=age_limits)
            executions = api.get_user_execution(
                id=user.profile.uid, date=startdate)

            for execution in executions:
                jobs = Job.objects.filter(
                    uid=execution.get("id"),
                    status=Status.objects.get(code=execution.get("status")))
                if jobs.count() > 0:
                    continue

                job = Job()
                job.start_date = execution.get("start_date", "")
                job.end_date = execution.get("end_date", "")
                job.progress = execution.get("progress", 0)

                results = execution.get("results")
                if results:
                    job.results = {"urls": results["urls"]}

                try:
                    job.script = models.ExecutionScript.objects.get(
                        uid=execution.get("script_id"))
                except Exception as e:
                    print(e)
                job.status = Status.objects.get(code=execution.get("status"))
                job.uid = execution.get("id")
                job.user = user
                job.user.profile.uid = execution.get("user_id", "")
                job.save()
                job.user.profile.save(update_fields=["uid"])

            if 'next' in self.request.POST:
                return HttpResponseRedirect(self.request.POST['next'])
            else:
                return HttpResponseRedirect(self.success_url)
        else:
            messages.add_message(self.request, messages.ERROR,
                                 'Wrong credentials please try again')
            return HttpResponseRedirect(reverse_lazy('login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        countries = models.Country.objects.all().order_by('name')
        context['countries'] = countries
        context['regions'] = models.Region.objects.filter(
            country=countries.first()).order_by("name")
        return context


class RegisterView(FormView):
    """Renders to the user registration view

    Returns:
        HTTP Response: HTML content with the user registration view
    """

    form_class = forms.SignupForm
    success_url = reverse_lazy('dashboard')
    template_name = 'account/register_page.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            print(form.errors)
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        api = Api(email=credentials['email'],
                  password=credentials['password1'])

        if api.token is not None:
            messages.add_message(self.request, messages.ERROR,
                                 'User with this credentials already exists!')
            return HttpResponseRedirect(reverse_lazy('login'))
        else:
            user = form.save(commit=False)
            user.username = credentials['email']
            user.is_active = True

            user.save()

            user.profile.country_id = int(self.request.POST.get('country'))
            user.profile.region_id = int(self.request.POST.get('region'))
            user.profile.organization = self.request.POST.get('organization')
            user.profile.role = models.Role.objects.get(code='USER')
            user.profile.save()

            chbox_mail = self.request.POST.get("chbox_mail")

            models.Settings.objects.update_or_create(
                in_mail_list=chbox_mail == "on", user=user)

            api = Api()
            api.register(email=user.email,
                         password=self.request.POST.get("password1"),
                         name=user.first_name + " " + user.last_name,
                         organization=user.profile.organization,
                         country=user.profile.country.name)

            user = authenticate(username=user.email,
                                password=self.request.POST.get("password1"))

            if user is not None:
                login(self.request, user)

                api = Api(email=user.email,
                          password=self.request.POST.get("password1"))

                self.request.session['bearer_token'] = api.token
                return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        countries = models.Country.objects.all().order_by('name')
        context['countries'] = countries
        context['regions'] = models.Region.objects.filter(
            country=countries.first()).order_by("name")
        return context


@ login_required
def update_user_details(request):
    if request.method == 'POST':
        if not request.session.get("bearer_token"):
            return HttpResponseRedirect(reverse_lazy('logout'))
        api = Api(token=request.session['bearer_token'])

        user = User.objects.get(id=int(request.POST.get("user_id")))
        form = forms.SignupForm(request.POST or None, instance=user)
        form.fields['password1'].required = False
        form.fields['password2'].required = False
        form.fields['username'].required = False
        form.fields['email'].required = False

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        if request.POST.get('is_active'):
            user.is_active = int(request.POST.get('is_active')) == 1

        fields = ['first_name', 'last_name', 'is_active']
        if len(form['password1'].value()) > 0:
            fields.append('password')
            user.password = make_password(form['password1'].value())
        if len(form['email'].value()) > 0:
            fields.append('email')
            fields.append('username')
            user.username = form['username'].value()
            user.email = form['email'].value()

        if form.is_valid():
            user.save(update_fields=fields)

            if request.POST.get('role'):
                user.profile.role_id = int(request.POST.get("role"))
            user.profile.organization = request.POST.get('organization')
            user.profile.country_id = int(request.POST.get('country'))
            user.profile.region_id = int(request.POST.get('region'))

            user.profile.save(
                update_fields=['organization', 'country_id', 'region_id',
                               'role_id'])

            api.update_user(email=user.email,
                            name=user.first_name + " " + user.last_name,
                            organization=user.profile.organization,
                            country=user.profile.country.name)

            return JsonResponse({"msg": "User details updated successfully!"},
                                status=200)

        else:
            print(form.error_messages)
            return JsonResponse({"msg": "Error updating user details"},
                                status=200)


def password_reset_view(request):
    template_name = 'account/password_reset.html'
    if request.POST:
        form = forms.PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            try:
                user = User.objects.get(email=data)
            except Exception as e:
                messages.add_message(
                    request, messages.ERROR,
                    'User with the email provided does not exist!')
                return render(request, template_name, {'form': form})
            subject = "Password Reset Requested"
            email_template_name = "messages/password_reset_email.txt"
            content = {
                "name": user.first_name + " " + user.last_name,
                "email": user.email,
                'domain': settings.SITE_HOST_NAME,
                'site_name': settings.SITENAME,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': settings.SITE_HOST_SCHEMA,
            }
            email = render_to_string(email_template_name, content)
            try:
                print(settings.DEFAULT_FROM_EMAIL)
                ret = send_mail(subject, email, from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=[user.email], fail_silently=False)
                print(ret, settings.EMAIL_USE_TLS, settings.EMAIL_ENABLE)
            except BadHeaderError as e:
                print(e)
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect(
                reverse_lazy('password_reset_done'))
    else:
        form = forms.PasswordResetForm
        return render(request, template_name, {'form': form})


@ login_required
def view_profile(request):
    """Load logged in user profile view
    """
    template = loader.get_template('account/profile_detail.html')

    context = {
        'user': request.user,
        'this_user': request.user,
        "parents": get_algorithms()
    }
    return HttpResponse(template.render(context, request))


@ login_required
def edit_profile(request):
    """Load logged in user profile update view
    """
    template = loader.get_template('account/edit_profile.html')
    countries = models.Country.objects.all().order_by('name')
    regions = models.Region.objects.filter(
        country=request.user.profile.country).order_by("name")

    roles = models.Role.objects.filter()
    context = {
        'this_user': request.user,
        'user': request.user,
        'countries': countries,
        "regions": regions,
        "parents": get_algorithms(),
        "roles": roles,
    }
    return HttpResponse(template.render(context, request))


@login_required
def view_user(request, user_id):
    """ Loads view for user details
    """
    template = loader.get_template('account/view_user.html')

    user = User.objects.get(pk=user_id)
    countries = models.Country.objects.all().order_by('name')
    regions = models.Region.objects.filter(
        country=user.profile.country).order_by("name")
    roles = models.Role.objects.filter()

    line_chart_data, pie_chart_data = get_chart_data(user)
    context = {
        'this_user': user,
        'user': request.user,
        'countries': countries,
        'regions': regions,
        'parents': get_algorithms(),
        'roles': roles,
        'line_chart_data': line_chart_data,
        'pie_chart_data': pie_chart_data
    }
    return HttpResponse(template.render(context, request))


@ login_required
def settings_view(request):
    template_name = 'account/settings.html'
    instance = None
    try:
        instance = models.Settings.objects.get(user=request.user)
    except Exception as e:
        pass
    if request.POST:
        form = forms.SettingsForm(instance=instance, data=request.POST)
        if form.is_valid():
            settings = form.save(commit=False)
            settings.user = request.user
            settings.save()
            messages.add_message(
                request, messages.SUCCESS,
                "Settings successfully updated!")
            return HttpResponseRedirect(reverse_lazy('settings'))
        messages.add_message(
            request, messages.ERROR,
            "Error occured while updating your settings!",
            fail_silently=True)
        return HttpResponseRedirect(reverse_lazy('settings'))
    else:
        form = forms.SettingsForm
        if instance is not None:
            form.base_fields["can_email_result"].initial = instance.can_email_result
            form.base_fields["in_mail_list"].initial = instance.in_mail_list
            form.base_fields["update_frequency_milliseconds"].initial = instance.update_frequency_milliseconds
            form.base_fields["buffer_checked"].initial = instance.buffer_checked
            form.base_fields["buffer_size"].initial = instance.buffer_size
            form.base_fields["data_age_limit"].initial = instance.data_age_limit

        return render(request, template_name,
                      {'form': form, "parents": get_algorithms()})


@ login_required
def admin_view(request):
    template = loader.get_template('account/admin.html')

    context = {
        'users_list': models.Profile.objects.filter(deleted=False),
        'jobs': Job.objects.filter(
            deleted=False,
            user=request.user,
            user__profile__deleted=False),
        "parents": get_algorithms(),
        "algorithms": get_algorithms(include_deleted=True)
    }
    return HttpResponse(template.render(context, request))


@ login_required
def view_feedback(request):
    """Loads a feedback form
    """
    template = loader.get_template('account/feedback.html')

    if request.POST:
        form = forms.FeedbackForm(data=request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()

            # Notify the admin
            subject = feedback.title
            email_template_name = "messages/feedback_text.txt"
            user = request.user
            content = {
                "sender": user.first_name + " " + user.last_name,
                "message": feedback.message,
                "email": user.email,
                "uid": user.profile.uid,
                "date": feedback.created_at
            }
            email = render_to_string(email_template_name, content)
            try:
                ret = send_mail(subject, html_message=email, message=email, from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=[settings.MAIL_TO_ADMIN], fail_silently=False)
            except BadHeaderError as e:
                print(e)

            # Notify the user of the receipt
            subject = "Reciept of your feedback: " + feedback.title
            email_template_name = "messages/feedback_sent_text.txt"
            user = request.user
            content = {
                "name": user.first_name + " " + user.last_name,
                "message": feedback.message,
                "title": feedback.title,
            }
            email = render_to_string(email_template_name, content)
            try:
                ret = send_mail(subject, html_message=email, message=email, from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=[user.email], fail_silently=False)
            except BadHeaderError as e:
                print(e)

            return HttpResponseRedirect(reverse_lazy('feedback'))
        else:
            messages.add_message(
                request, messages.ERROR,
                "Error occured while sending your message! Required fields cannot be empty.",
                fail_silently=True)
            return HttpResponseRedirect(reverse_lazy('feedback'))

    else:
        context = {
            'user': request.user,
            "parents": get_algorithms()
        }
        return HttpResponse(template.render(context, request))


def ajax_register_user(request):
    """Create a new user
    """
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True

            user.save()

            user.profile.country_id = int(request.POST.get('country'))
            user.profile.region_id = int(request.POST.get('region'))
            user.profile.organization = request.POST.get('organization')

            user.profile.save()

            api = Api()
            api.register(email=user.email,
                         password=request.POST.get("password1"),
                         name=user.first_name + " " + user.last_name,
                         organization=user.profile.organization,
                         country=user.profile.country.name)

            user = authenticate(username=user.email,
                                password=request.POST.get("password1"))

            if user is not None:
                login(request, user)

            api = Api(email=user.email,
                      password=request.POST.get("password1"))

            request.session['bearer_token'] = api.token
            return JsonResponse({"url": "/dashboard",
                                 "msg": "Account successfully created!"},
                                status=200)
        else:
            return HttpResponse(form.errors, status=300)


def ajax_get_regions(request):
    regions = models.Region.objects.filter(
        country_id=request.GET.get("country_id")).order_by("name")
    options = '<option value="0" data-rel="All regions">All regions</option>'
    for region in regions:
        options += "<option value='{}'>{}</option>".format(
            region.id, region.name)

    return HttpResponse(options)


def ajax_get_cities(request):
    cities = models.City.objects.filter(
        country_id=request.GET.get("country_id")).order_by("name_en")
    options = '<option value="0" data-rel="All cities">All cities</option>'
    for city in cities:
        options += "<option value='{}'>{}</option>".format(
            city.id, city.name_en)

    return HttpResponse(options)


@ login_required
def ajax_change_aoi(request):
    if request.POST:
        city, region, country = None, None, None
        lat, lon = None, None
        buffer_size = None
        file, uploaded_file_path = None, None
        aoi_id, geom = None, None

        area_name = request.POST.get("name")

        if request.POST.get("aoi_id") != "null":
            aoi = models.Aoi.objects.get(
                id=int(request.POST.get("aoi_id")))
        else:
            aoi = models.Aoi()
            aoi.name = area_name
            aoi.user = request.user

            if request.POST.get("country") != "null":
                country = models.Country.objects.get(
                    id=request.POST.get("country"))
                aoi.country = country
                geom = country.geom
                geom = geom.envelope

            if request.POST.get("city") != "null":
                city_id = int(request.POST.get("city"))
                if city_id > 0:
                    city = models.City.objects.get(id=city_id)
                    aoi.city = city
                    geom = city.geom

            if request.POST.get("region") != "null":
                region_id = int(request.POST.get("region"))
                if region_id > 0:
                    region = models.Region.objects.get(
                        id=region_id)
                    aoi.region = region
                    geom = region.geom

            if request.POST.get("lat") != "null":
                lat = float(request.POST.get("lat"))
                lon = float(request.POST.get("lon"))
                geom = Point(lon, lat, srid=4326)

            if request.POST.get("file") != "null":
                file = request.FILES["file"]
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                uploaded_file_path = fs.path(filename)

                # ds = ogr.Open(uploaded_file_path)
                # layer = ds.GetLayer()
                # extent = layer.GetExtent()
                # geom = Polygon.from_bbox(extent)

                # layer = None
                # ds = None

                # if uploaded_file_path is not None:
                #     fs.delete(uploaded_file_path)

            if request.POST.get("buffer_size") != "null":
                buffer_size = float(request.POST.get("buffer_size"))
                distance = buffer_size * 1000
                buffer_width = distance / 40000000.0 * 360.0
                geom = geom.buffer(buffer_width)

                aoi.buffer_size = buffer_size
            if geom.area < 3000:
                aoi.geom = geom
                aoi.save()
            else:
                print(geom.area)
                return JsonResponse({"msg": "Selected area of interest larger than the threshold of 20 million sq.km !"}, status=400)

        return JsonResponse({"msg": "Region of interest updated!", "id": aoi.id, "name": aoi.name}, status=200)


@ login_required
def ajax_upload_profile_image(request):
    if request.POST:
        fs = FileSystemStorage()
        profile = models.Profile.objects.get(
            user_id=int(request.POST.get("user_id")))

        file = request.FILES["file"]
        filename = fs.save(file.name, file)
        uploaded_file_path = fs.path(filename)

        if os.path.exists(uploaded_file_path):
            if profile.photo != "":
                fs.delete(profile.photo)

            profile.photo = filename
            profile.save(update_fields=['photo'])
            print(uploaded_file_path)
            return JsonResponse({"image": filename,
                                "msg": "Profile photo updated!"}, status=200)
        else:
            return JsonResponse(
                {"msg": "Profile photo not uploaded!"}, status=400)


@login_required
def ajax_update_algorithms_visibility(request):
    if request.POST:
        form_data = request.POST.get("data")
        form_data = json.loads(form_data)
        for data in form_data:
            if data["typeof"] == "algorithm":
                algos = models.Algorithm.objects.filter(
                    id=data['id'])
            else:
                algos = models.Algorithm.objects.filter(
                    scripts__in=[models.Script.objects.get(id=data['id'])])
            for algo in algos:
                algo.deleted = not data["checked"]
                algo.save(update_fields=["deleted"])
                scripts = algo.scripts.all()
                for script in scripts:
                    script.execution_script.version = data["version"]
                    script.execution_script.save(update_fields=["version"])

        return JsonResponse({
            "msg": "Settings updated!"}, status=200)
    else:
        return JsonResponse({
            "msg": "Settings not updated!"}, status=400)


def get_user_aoi(user, srid=3857):
    features = []
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT name, st_asgeojson(st_transform(geom, {})) as geom
                FROM area_of_interest
                WHERE user_id = {}
                """.format(srid, user.id))
        geoms = dictfetchall(cursor)

        features = []
        for geom in geoms:
            features.append(
                {
                    "type": "Feature",
                    "geometry": json.loads(geom["geom"]),
                    "properties": {"name": geom["name"]}
                })

    return {
        "type": "FeatureCollection",
        "features": features,
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::" + str(srid)}}
    }


@login_required
def ajax_load_aoi(request):
    srid = 3857
    if request.GET.get("srid"):
        srid = request.GET.get("srid")

    geojson = get_user_aoi(request.user, srid)
    return JsonResponse(
        geojson,
        safe=False)


def get_chart_data(user=None):

    line_chart_data = []
    pie_chart_data = []
    with connection.cursor() as cursor:
        where = " WHERE user_id ={}".format(
            user.id) if user is not None else ""
        cursor.execute("""
            SELECT distinct 1000 * EXTRACT(EPOCH FROM DATE(a.start_date))::bigint AS date
            FROM jobs AS a
            {}
            ORDER BY 1 ASC
        """.format(where))
        dates = dictfetchall(cursor)

        cursor.execute("""
            SELECT distinct b.id, b.name_readable as name
            FROM jobs AS a
                JOIN execution_script AS b ON a.script_id = b.id
            {}
            ORDER BY 2;
        """.format(where))

        scripts = dictfetchall(cursor)

        for script in scripts:
            for date in dates:
                where = " AND user_id ={} ".format(
                    user.id) if user is not None else ""

                where += " AND a.script_id = {} AND (1000 * EXTRACT(EPOCH FROM DATE(a.start_date)))::bigint = {}::bigint".format(
                    script["id"], date["date"])
                query = """
                    SELECT count(*), 1000 * EXTRACT(EPOCH FROM DATE(a.start_date)) AS date, b.name_readable AS name, b.id as code
                    FROM jobs AS a
                        JOIN execution_script AS b ON a.script_id = b.id
                    {}
                    GROUP BY 2, 3, 4
                    ORDER BY 3,2;""".format(where)
                cursor.execute(query)
                result = dictfetchall(cursor)
                if len(result) > 0:
                    line_chart_data.append(result[0])
                else:
                    line_chart_data.append({
                        "count": 0,
                        "date": date["date"],
                        "name": script["name"],
                        "code": script["id"]
                    })

        where = " WHERE user_id ={}".format(
            user.id) if user is not None else ""
        cursor.execute("""
                SELECT count(*) as value, b.name_readable as name, b.id as code  FROM jobs AS a
                JOIN execution_script AS b ON a.script_id = b.id
                {}
                GROUP BY 2, 3
                ORDER BY 2;
            """.format(where))
        pie_chart_data = dictfetchall(cursor)
    return line_chart_data, pie_chart_data


def get_algorithms(include_deleted=False):
    if include_deleted:
        parents = models.Algorithm.objects.filter(
            parent_id=None).values().order_by("id")
    else:
        parents = models.Algorithm.objects.filter(
            parent_id=None, deleted=False).values().order_by("id")
    algorithms = []
    for parent in parents:
        children = models.Algorithm.objects.filter(
            parent_id=parent['id'], uid=None)
        if children.count() > 0:
            parent["children"] = children
        algorithms.append(parent)
    return algorithms
