from datetime import datetime
import urllib.request
import json
import os
from django import urls
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseRedirect
)
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from account import models as accountmodels
from job.models import Job, Status
from utils.api import Api

from . import models
from utils.util import (matrix_to_table, url_exists)
from utils import conf
from account.views import get_chart_data, signout, get_algorithms


@login_required
def dashboard(request):
    template = loader.get_template('core/index.html')

    line_chart_data, pie_chart_data = get_chart_data()
    context = {
        "parents": get_algorithms(),
        'line_chart_data': line_chart_data,
        'pie_chart_data': pie_chart_data
    }
    return HttpResponse(template.render(context, request))


@login_required
def view_algorithm(request, algo_id):
    template = loader.get_template('core/algorithm.html')
    parents = accountmodels.Algorithm.objects.filter(
        parent_id=None, deleted=False).values().order_by("id")

    countries = accountmodels.Country.objects.all().order_by('name')
    regions = accountmodels.Region.objects.filter(
        country=countries.first()).order_by("name")
    cities = accountmodels.City.objects.filter(
        country=countries.first()).order_by("name_en")
    aoi = accountmodels.Aoi.objects.filter(user=request.user)
    if aoi.count() > 0:
        aoi = aoi.first()
        if aoi.country:
            regions = accountmodels.Region.objects.filter(
                country=aoi.country).order_by("name")
            cities = accountmodels.City.objects.filter(
                country=aoi.country).order_by("name_en")
    else:
        aoi = None

    context = {
        "parents":  get_algorithms(),
        "children":  accountmodels.Algorithm.objects.filter(
            parent_id=algo_id, deleted=False).order_by("id"),
        "id": algo_id,
        "table": matrix_to_table(),
        "agg_table": create_aggregation_table(request),
        "jrc_lpd_datasets": list(
            conf.REMOTE_DATASETS["Land Productivity Dynamics (JRC)"].keys()),
        "regions": regions,
        "countries": countries,
        "cities": cities,
        "aoi": aoi,
        "conf": conf.REMOTE_DATASETS

    }
    return HttpResponse(template.render(context, request))


@login_required
def ajax_update_aggregation_method(request):
    if request.POST:
        models.UserAggregationClass.objects.filter(user=request.user).delete()
        form_data = request.POST.get("tdata")
        form_data = json.loads(form_data)
        for array in form_data:
            user_aggregate = models.UserAggregationClass()
            user_aggregate.inputclass_id = array.get("inputclass")
            user_aggregate.outputclass_id = array.get("outputclass")
            user_aggregate.user = request.user
            user_aggregate.save()
        return JsonResponse({"msg": "Updated Aggregation Definition"},
                            status=200)


def create_aggregation_table(request):
    agg_classes = models.UserAggregationClass.objects.filter(user=request.user)
    if agg_classes.count() == 0:
        agg_classes = models.UserAggregationClass.objects.filter(
            user_id=None).exclude(inputclass__code='-32768')
    agg_output_classes = models.AggregationOutputClass.objects.filter()\
        .exclude(
        code='-32768')

    table = """
        <table class="display" id="aggregation_definition_tbl"
            style="width:100%">
            <thead>
                <tr>
                    <th style="width: 20%;">Input Code</th>
                    <th style="width: 50%;">Input Class</th>
                    <th style="width: 30%;">Output Class</th>
                </tr>
            </thead>
            <tbody>"""
    for row in agg_classes:
        if row.inputclass.code == '-32768':
            continue
        table += """<tr >
           <td>
              {}
            </td >
            <td >
              {}
            </td >
            <td>
                <input type="hidden" value="{}">
                <select class = "js-states form-select" >""".format(
            row.inputclass.code, row.inputclass.name_long, row.inputclass.id)

        for opt in agg_output_classes:
            if row.outputclass.code == opt.code:
                table += """<option selected value = "{}" >
                                {}
                            </option >
                        """.format(opt.id, opt.name_long)
            else:
                table += """
                    <option value = "{}" >
                        {}
                    </option >
                    """.format(opt.id, opt.name_long)
        table += """
                </select >
            </td >
        </tr >"""
    table += "</tbody></table>"
    return table


@login_required
def ajax_get_runmode(request, id):
    scripts = accountmodels.Algorithm.objects.get(
        id=id, deleted=False).scripts.all()
    runmodes = []
    options = ""
    for script in scripts:
        runmode = script.execution_script.run_mode
        runmodes.append({"id": runmode.id, "value":  runmode.value})
        options += "<option value='{}'>{}</option>".format(
            runmode.id, runmode.value)
    return JsonResponse({"runmodes": runmodes, "options": options})


@login_required
def ajax_get_algorithm_view(request, id, runmode):
    if runmode < 1:
        script = accountmodels.ExecutionScript.objects.filter(
            deleted=False,
            script__in=[obj.id for obj in accountmodels.Script.objects.filter(
                algorithm__id=id)])
    else:
        script = accountmodels.ExecutionScript.objects.filter(
            deleted=False,
            run_mode_id=runmode,
            script__in=[obj.id for obj in accountmodels.Script.objects.filter(
                algorithm__id=id)])

    countries = accountmodels.Country.objects.all().order_by('name')
    regions = accountmodels.Region.objects.filter(
        country=countries.first()).order_by("name")

    cities = accountmodels.City.objects.filter(
        country=countries.first()).order_by("name_en")

    aoi = accountmodels.Aoi.objects.filter(user=request.user)
    if aoi.count() > 0:
        aoi = aoi.first()
        if aoi.country:
            regions = accountmodels.Region.objects.filter(
                country=aoi.country).order_by("name")
            cities = accountmodels.City.objects.filter(
                country=aoi.country).order_by("name_en")
    else:
        aoi = None

    context = {
        "table": matrix_to_table(),
        "jrc_lpd_datasets": list(
            conf.REMOTE_DATASETS["Land Productivity Dynamics (JRC)"]
            .keys()),
        "agg_table": create_aggregation_table(request),
        "regions": regions,
        "countries": countries,
        "cities": cities,
        "script": script.first(),
        "aoi": aoi,
        "conf": conf.REMOTE_DATASETS
    }

    if script.first().name == "productivity":
        trajectory_functions = {'NDVI trends': {'climate types': [],
                                                'description': 'Calculate trend of annually integrated NDVI.',
                                                'params': {'trajectory_method': 'ndvi_trend'}},
                                'Pixel RESTREND': {'climate types': ['Precipitation', 'Soil moisture',
                                                                     'Evapotranspiration'], 'description': 'Calculate pixel residual trend (RESTREND of annually integrated NDVI, after removing trend associated with a climate indicator.', 'params': {
                                    'trajectory_method': 'p_restrend'}}, 'Rain Use Efficiency (RUE)': {'climate types': ['Precipitation'], 'description': 'Calculate rain use efficiency (precipitation divided by NDVI).', 'params': {'trajectory_method': 'ue'}}, 'Water Use Efficiency (WUE)': {'climate types': ['Evapotranspiration'], 'description': 'Calculate water use efficiency (evapotranspiration divided by NDVI).', 'params': {'trajectory_method': 'ue'}}}
        # trajectory_functions = json.loads(additional_configuration)
        context["trajectory_functions"] = list(trajectory_functions.keys())
        climate_datasets = []
        climate_types = trajectory_functions["NDVI trends"]["climate types"]
        for climate_type in climate_types:
            climate_datasets + list(conf.REMOTE_DATASETS[climate_type].keys())
        context["climate_datasets"] = climate_datasets
    if script.count() > 0:
        return render(
            request, 'core/forms/' + script.first().name + ".html", context
        )


def ajax_get_matrix_table(request):
    return HttpResponse(matrix_to_table(), status=200)


def ajax_reset_aggregation_table(request):
    models.UserAggregationClass.objects.filter(user=request.user).delete()
    defaults = models.UserAggregationClass.objects.filter(
        user_id=None)
    for default in defaults:
        models.UserAggregationClass.objects.create(
            user=request.user, inputclass=default.inputclass,
            outputclass=default.outputclass)

    return HttpResponse(create_aggregation_table(request), status=200)


def getjobs(request, script_id):
    jobs = Job.objects.filter(
        user=request.user, script_id=script_id, deleted=False)
    if not 'bearer_token' in request.session:
        signout(request)

    api = Api(token=request.session['bearer_token'])
    job_result = []
    for job in jobs:
        if job.status.value in ("PENDING", "RUNNING", "READY"):
            currentjob = api.get_execution(job.uid)
            job.progress = currentjob["progress"]
            job.end_date = currentjob["end_date"]
            job.status = Status.objects.get(code=currentjob["status"])
            job.results = currentjob["results"]
            job.save(update_fields=["progress",
                                    "end_date", "status", "results"])
        job_result.append(job)
    return job_result


@login_required
def ajax_load_results(request, script_id):
    template = loader.get_template('core/jobs.html')
    context = {
        "jobs": getjobs(request, script_id)
    }
    return HttpResponse(template.render(context, request))


@login_required
def ajax_download_job(request, uid):
    job = Job.objects.get(user=request.user, uid=uid, deleted=False)
    urls = job.results["urls"]
    if len(urls) == 1:
        if url_exists(urls[0]["url"]):
            return JsonResponse({"url": urls[0]["url"]}, status=200)
        else:
            return JsonResponse({"msg": "File not found"}, status=400)

    date = datetime.now()
    filename = "../" + \
        str(date.timestamp) + job.results.name + ".zip"
    with open(filename, "wb") as fout:
        for url in urls:
            response = urllib.request.urlopen(url["url"])
            # filename = response.headers.get(
            #     "Content-Disposition").split("filename=")[1]
            fout.write(response.read())
    if os.path.exists(filename):
        return JsonResponse({"url": "/media/" + filename,
                             "fname": filename}, status=200)
    else:
        return JsonResponse({"msg": "File not found"}, status=400)


@login_required
def ajax_cancel_job(request, uid):
    job = Job.objects.get(user=request.user, uid=uid, deleted=False)
    job.status = Status.objects.get(code="CANCELLED")
    job.save(update_fields=['status'])
    # api = Api(token=request.session['bearer_token'])
    return JsonResponse({"msg": "Job cancelled successfully"}, status=200)


@login_required
def ajax_delete_job(request, uid):
    # api = Api(token=request.session['bearer_token'])

    try:
        job = Job.objects.get(user=request.user, uid=uid, deleted=False)
        job.deleted = True
        job.status = Status.objects.get(code="DELETED")
        job.save(update_fields=['deleted', 'status'])
        return JsonResponse({"msg": "Job deleted successfully"}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"msg": "Job not found"}, status=400)


@login_required
def ajax_load_climate_dataset(request):
    script = accountmodels.ExecutionScript.objects.get(
        name=request.GET.get("algo"), deleted=False)
    if script.name == "productivity":
        additional_configuration = script.additional_configuration
        additional_configuration = additional_configuration.replace("'", '"')
        trajectory_functions = json.loads(additional_configuration)
        climate_datasets = []
        climate_types = trajectory_functions[request.GET.get(
            "indicator")]["climate types"]
        for climate_type in climate_types:
            climate_datasets += list(conf.REMOTE_DATASETS[climate_type].keys())

        options = ""
        for data in climate_datasets:
            options += "<option value='{}'>{}</option>".format(data, data)
        return HttpResponse(options)
