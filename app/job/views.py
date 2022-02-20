from datetime import datetime

import urllib.request
import json
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    JsonResponse
)
from django.template import loader
from te_schemas.productivity import ProductivityMode
from te_schemas.land_cover import LCTransitionDefinitionDeg, LCLegendNesting
from job.models import Job, Status

from utils.util import table_to_matrix, get_lc_nesting, get_trans_matrix
from account import models as accountmodels
from account.views import logout
from core import models as coremodels
from core import views
from utils import conf
from utils.api import Api
from utils.logger import log
from utils.util import url_exists, get_styles


def index(request):
    pass


def get_nestings(request):
    agg_classes = coremodels.UserAggregationClass.objects.filter(
        user=request.user)
    if agg_classes.count() == 0:
        agg_classes = coremodels.UserAggregationClass.objects.filter(
            user_id=None).exclude(inputclass__code='-32768')
    input_classes = coremodels.AggregationInputClass\
        .objects.filter()\
        .exclude(
            code='-32768')
    output_classes = coremodels.AggregationOutputClass\
        .objects.filter()\
        .exclude(
            code='-32768')

    input_key = []
    for child in input_classes:
        input_key.append({
            "code": int(child.code),
            "color": child.color,
            "description": child.description,
            "name_long": child.name_long,
            "name_short": child.name_short
        })

    output_key = []
    for child in output_classes:
        output_key.append({
            "code": int(child.code),
            "color": child.color,
            "description": child.description,
            "name_long": child.name_long,
            "name_short": child.name_short
        })

    nestings = {
        "-32768": [
            -32768
        ],
    }
    for agg in agg_classes:
        if agg.outputclass.code not in nestings:
            nestings[agg.outputclass.code] = [int(agg.inputclass.code)]
        else:
            nestings[agg.outputclass.code].append(int(agg.inputclass.code))

    nesting = {
        "child": {
            "key": input_key,
            "name": "ESA CCI Land Cover",
                    "nodata": {
                        "code": -32768,
                        "color": "#000000",
                        "description": None,
                        "name_long": "No data",
                        "name_short": "No data"
                    }
        },
        "parent": {
            "key": output_key,
            "name": "UNCCD Land Cover",
                    "nodata": {
                        "code": -32768,
                        "color": "#000000",
                        "description": None,
                        "name_long": "No data",
                        "name_short": "No data"
                    }
        },
        "nesting": nestings
    }
    return nesting


def process_land_cover(request):
    form_data = request.POST.get("tdata")
    form_data = json.loads(form_data)
    matrix = table_to_matrix(form_data)
    matrix = LCTransitionDefinitionDeg.Schema().dumps(matrix)

    task_name = request.POST.get("task_name")

    aoi_id = int(request.POST.get("aoi_id"))
    aoi = accountmodels.Aoi.objects.get(id=aoi_id)
    geom = aoi.geom
    payload = {
        "year_initial": int(request.POST.get("initial_year_de")),
        "year_final": int(request.POST.get("target_year_de")),
        'geojsons': json.dumps([json.loads(geom.json)]),
        'crs': str(geom.crs),
        'crosses_180th': False,
        'legend_nesting': get_nestings(request),
        'trans_matrix': json.loads(matrix),
        'task_name': task_name,
        'task_notes': request.POST.get("task_notes"),
    }
    return [payload]


def process_soc(request):
    task_name = request.POST.get("task_name")
    matrix = LCTransitionDefinitionDeg.Schema().dumps(get_trans_matrix())

    aoi_id = int(request.POST.get("aoi_id"))
    aoi = accountmodels.Aoi.objects.get(id=aoi_id)
    geom = aoi.geom
    payload = {
        "year_initial": int(request.POST.get("initial_year_de")),
        "year_final": int(request.POST.get("target_year_de")),
        'fl': request.POST.get("climate_regime"),
        'download_annual_lc': request.POST.get("download_annual_lc") == "true",
        'geojsons': json.dumps([json.loads(geom.json)]),
        'crs': str(geom.crs),
        'crosses_180th': False,
        'legend_nesting': get_nestings(request),
        'trans_matrix': json.loads(matrix),
        'task_name': task_name,
        'task_notes': request.POST.get("task_notes"),
    }
    return [payload]


def process_drought_vulnerability(request):
    population_dataset_name = "Gridded Population Count"
    population_dataset = conf.REMOTE_DATASETS["WorldPop"][population_dataset_name]

    spi_dataset_name = "GPCC V6 (Global Precipitation Climatology Centre)"
    spi_dataset = conf.REMOTE_DATASETS["SPI"][spi_dataset_name]

    aoi_id = int(request.POST.get("aoi_id"))
    aoi = accountmodels.Aoi.objects.get(id=aoi_id)
    geom = aoi.geom

    payload = {}
    payload['population'] = {
        'asset': population_dataset['GEE Dataset'],
        'source': population_dataset_name
    }

    payload['spi'] = {
        'asset': spi_dataset['GEE Dataset'],
        'source': spi_dataset_name,
        'lag': int(request.POST.get("lag_cb"))
    }

    payload.update({
        'geojsons': [json.loads(geom.json)],
        'crs': str(geom.crs),
        'crosses_180th': False,
        'task_name': request.POST.get("task_name"),
        'task_notes': request.POST.get("task_notes"),
        'year_initial': int(request.POST.get("initial_year_de")),
        'year_final': int(request.POST.get("target_year_de")),
    })
    return [payload]


def process_unccd_reporting(request):
    population_dataset_name = "Gridded Population Count"
    population_dataset = conf.REMOTE_DATASETS["WorldPop"][population_dataset_name]

    spi_dataset_name = "GPCC V6 (Global Precipitation Climatology Centre)"
    spi_dataset = conf.REMOTE_DATASETS["SPI"][spi_dataset_name]

    aoi_id = int(request.POST.get("aoi_id"))
    aoi = accountmodels.Aoi.objects.get(id=aoi_id)
    geom = aoi.geom

    payload = {}
    payload['population'] = {
        'asset': population_dataset['GEE Dataset'],
        'source': population_dataset_name
    }

    payload['spi'] = {
        'asset': spi_dataset['GEE Dataset'],
        'source': spi_dataset_name,
        'lag': int(request.POST.get("lag_cb"))
    }

    payload.update({
        'geojsons': [json.loads(geom.json)],
        'crs': str(geom.crs),
        'crosses_180th': False,
        'task_name': request.POST.get("task_name"),
        'task_notes': request.POST.get("task_notes"),
        'year_initial': int(request.POST.get("initial_year_de")),
        'year_final': int(request.POST.get("target_year_de")),
    })

    return [payload]


def process_urban_change(request):
    aoi_id = int(request.POST.get("aoi_id"))
    aoi = accountmodels.Aoi.objects.get(id=aoi_id)
    geom = aoi.geom

    payload = {
        'un_adju': request.POST.get("un_adju"),
        'isi_thr': request.POST.get("isi_thr"),
        'ntl_thr': request.POST.get("ntl_thr"),
        'wat_thr': request.POST.get("wat_thr"),
        'cap_ope': request.POST.get("cap_ope"),
        'pct_suburban': request.POST.get("pct_suburban"),
        'pct_urban': request.POST.get("pct_urban"),
        'geojsons': json.dumps([json.loads(geom.json)]),
        'crs': str(geom.crs),
        'crosses_180th': False,
        'task_name': request.POST.get("task_name"),
        'task_notes': request.POST.get("task_notes"),
    }

    return [payload]


def process_restoration_biomass(request):
    aoi_id = int(request.POST.get("aoi_id"))
    aoi = accountmodels.Aoi.objects.get(id=aoi_id)
    geom = aoi.geom

    payload = {
        'length_yr': request.POST.get("length_yr"),
        'rest_type': request.POST.get("rest_type"),
        'geojsons': json.dumps([json.loads(geom.json)]),
        'crs': str(geom.crs),
        'crosses_180th': False,
        'task_name': request.POST.get("task_name"),
        'task_notes': request.POST.get("task_notes"),
    }

    return [payload]


def process_total_carbon(request):
    aoi_id = int(request.POST.get("aoi_id"))
    aoi = accountmodels.Aoi.objects.get(id=aoi_id)
    geom = aoi.geom

    payload = {
        'year_initial': int(request.POST.get("year_initial")),
        'year_final': int(request.POST.get("year_final")),
        'fc_threshold': float(request.POST.get("fc_threshold")),
        'method': request.POST.get("method"),
        'biomass_data': request.POST.get("biomass_data"),
        'geojsons': json.dumps([json.loads(geom.json)]),
        'crs': str(geom.crs),
        'crosses_180th': False,
        'task_name': request.POST.get("task_name"),
        'task_notes': request.POST.get("task_notes"),
    }

    print(payload)

    return [payload]


def process_land_productivity(request, script):
    if request.POST:
        ndvi_dataset = conf.REMOTE_DATASETS[
            'NDVI'][request.POST.get("ndvi_dataset")]['GEE Dataset']

        additional_configuration = script.additional_configuration
        additional_configuration = additional_configuration.replace(
            "'", '"')
        trajectory_functions = json.loads(
            additional_configuration).get("trajectory functions")

        climate_gee_dataset = None
        if request.POST.get("traj_climate") != 'null':
            climate_datasets = {}
            climate_types = trajectory_functions[request.POST.get(
                "trajectory_indicator")]["climate types"]
            for climate_type in climate_types:
                climate_datasets.update(conf.REMOTE_DATASETS[climate_type])
            climate_gee_dataset = climate_datasets[request.POST.get(
                "traj_climate")]['GEE Dataset']
            log(u'climate_gee_dataset {}'.format(climate_gee_dataset))

        task_name = request.POST.get("task_name")
        aoi_id = int(request.POST.get("aoi_id"))
        aoi = accountmodels.Aoi.objects.get(id=aoi_id)
        geom = aoi.geom

        prod_mode = ProductivityMode.TRENDS_EARTH_5_CLASS_LPD.value if request.POST.get(
            "prod_mode") == 1 else ProductivityMode.JRC_5_CLASS_LPD.value

        payload = {
            'prod_mode': prod_mode,
            'calc_traj': request.POST.get("calc_traj"),
            'calc_perf': request.POST.get("calc_perf"),
            'calc_state': request.POST.get("calc_state"),
            'prod_traj_year_initial': request.POST.
            get("prod_traj_year_initial"),
            'prod_traj_year_final': request.POST.get("prod_traj_year_final"),
            'prod_perf_year_initial': request.POST.
            get("prod_perf_year_initial"),
            'prod_perf_year_final': request.POST.get("prod_perf_year_final"),
            'prod_state_year_bl_start': request.POST
            .get("prod_state_year_bl_start"),
            'prod_state_year_bl_end': request.POST.
            get("prod_state_year_bl_end"),
            'prod_state_year_tg_start': request.POST.
            get("prod_state_year_tg_start"),
            'prod_state_year_tg_end': request.POST.
            get("prod_state_year_tg_end"),
            'geojsons': json.dumps([json.loads(geom.json)]),
            'crs': str(geom.crs),
            'crosses_180th': False,
            'ndvi_gee_dataset': ndvi_dataset,
            'climate_gee_dataset': climate_gee_dataset,
            'task_name': task_name,
            'task_notes': request.POST.get("task_notes"),
        }

        if request.POST.get("trajectory_indicator") is not None:
            current_trajectory_function = trajectory_functions[
                request.POST.get("trajectory_indicator")]
            payload.update(current_trajectory_function["params"])
        return [payload]


def process_sub_indicators(request, script):
    if request.POST:
        form_data = request.POST.get("tdata")
        form_data = json.loads(form_data)
        matrix = table_to_matrix(form_data)
        matrix = LCTransitionDefinitionDeg.Schema().dumps(matrix)
        periods = json.loads(request.POST.get("periods"))
        prod_mode = ProductivityMode.TRENDS_EARTH_5_CLASS_LPD.value if request.POST.get(
            "prod_mode") == 1 else ProductivityMode.JRC_5_CLASS_LPD.value

        payloads = []
        for period, values in periods.items():
            payload = {}
            year_initial = values['period_year_initial']
            year_final = values['period_year_final']

            payload['productivity'] = {
                'mode': prod_mode
            }

            if prod_mode == ProductivityMode.TRENDS_EARTH_5_CLASS_LPD.value:
                prod_state_year_bl_start = year_initial
                prod_state_year_bl_end = year_final - 3
                prod_state_year_tg_start = prod_state_year_bl_end + 1
                prod_state_year_tg_end = prod_state_year_bl_end + 3
                assert prod_state_year_tg_end == year_final

                payload['productivity'].update({
                    'prod_asset': conf.REMOTE_DATASETS["NDVI"]["MODIS (MOD13Q1, annual)"]["GEE Dataset"],
                    'traj_method': 'ndvi_trend',
                    'traj_year_initial': year_initial,
                    'traj_year_final': year_final,
                    'perf_year_initial': year_initial,
                    'perf_year_final': year_final,
                    'state_year_bl_start': prod_state_year_bl_start,
                    'state_year_bl_end': prod_state_year_bl_end,
                    'state_year_tg_start': prod_state_year_tg_start,
                    'state_year_tg_end': prod_state_year_tg_end,
                    'climate_asset': None,
                })
            else:
                if period == 'baseline':
                    prod_dataset = conf.REMOTE_DATASETS["Land Productivity Dynamics (JRC)"][request.POST.get(
                        "cb_jrc_baseline")]
                else:
                    prod_dataset = conf.REMOTE_DATASETS["Land Productivity Dynamics (JRC)"][request.POST.get(
                        "cb_jrc_progress")]
                prod_asset = prod_dataset['GEE Dataset']
                prod_start_year = prod_dataset['Start year']
                prod_end_year = prod_dataset['End year']
                payload['productivity'].update({
                    'prod_asset': prod_asset,
                    'year_initial': prod_start_year,
                    'year_final': prod_end_year
                })

            payload['land_cover'] = {
                'year_initial': year_initial,
                'year_final': year_final,
                'legend_nesting': get_nestings(request),
                'trans_matrix': json.loads(matrix),
            }
            payload['soil_organic_carbon'] = {
                'year_initial': year_initial,
                'year_final': year_final,
                'fl': .80,
                'legend_nesting': get_nestings(request),
                'trans_matrix': json.loads(matrix),
            }

            payload['population'] = {
                'year': year_final,
                'population_asset': "users/geflanddegradation/toolbox_datasets/worldpop_ppp_2000_2020_1km_global",
                'population_source_name': "WorldPop"
            }

            task_name = request.POST.get("task_name")

            if len(periods.items()) == 2:
                if task_name:
                    task_name = f'{task_name} - {period}'
                else:
                    task_name = f'{period}'

            aoi_id = int(request.POST.get("aoi_id"))
            aoi = accountmodels.Aoi.objects.get(id=aoi_id)
            geom = aoi.geom

            payload.update({
                'geojsons': [json.loads(geom.json)],
                'crs': str(geom.crs),
                'crosses_180th': False,
                'task_name': task_name,
                'task_notes': request.POST.get("task_notes"),
                'period': {
                    'name': period,
                    'year_initial': year_initial,
                    'year_final': year_final
                },
                'script': {
                    'id': script.uid,
                    'version': script.version,
                    'execution_callable': '',
                    'description': script.description,
                    'additional_configuration': {},
                    'run_mode': "remote",
                    'name': script.name,
                    'name_readable': script.name_readable,
                    'slug': script.name
                },
                'local_context': {
                    'area_of_interest_name': aoi.name,
                    'base_dir': ''}
            })

            payload["local_context"] = {}
            payloads.append(payload)
    return payloads


@ login_required
def ajax_run_job(request):
    if request.POST:
        algo_name = request.POST.get("algo")
        script = accountmodels.Script.objects.get(
            name=algo_name,
            run_mode="remote")
        if algo_name == "productivity":
            payloads = process_land_productivity(request, script)
        elif algo_name == "sdg-15-3-1-sub-indicators":
            payloads = process_sub_indicators(request, script)
        elif algo_name == "land-cover":
            payloads = process_land_cover(request)
        elif algo_name == "soil-organic-carbon":
            payloads = process_soc(request)
        elif algo_name == "drought-vulnerability":
            payloads = process_drought_vulnerability(request)
        elif algo_name == "urban-area":
            payloads = process_urban_change(request)
        elif algo_name == "unccd-report":
            payloads = process_unccd_reporting(request)
        elif algo_name == "restoration-biomass":
            payloads = process_restoration_biomass(request)
        elif algo_name == "total-carbon":
            payloads = process_total_carbon(request)

        api = Api(token=request.session['bearer_token'])

        for payload in payloads:
            if payload["crs"] == 'None':
                payload["crs"] = "GEOGCS[\"unknown\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]]]"
            url_fragment = f"/api/v1/script/{script.uid}/run"
            response = api.call_api(url_fragment, "post",
                                    payload, use_token=True)

            if response is not None:
                try:
                    out = response["data"]
                    out["params"] = ""
                    job = Job()
                    job.start_date = out.get("start_date", "")
                    job.end_date = out.get("end_date", "")
                    job.progress = out.get("progress", 0)
                    job.script = script
                    job.status = Status.objects.get(code=out.get("status"))
                    job.uid = out.get("id", "")
                    job.task_name = payload.get("task_name")
                    job.task_notes = payload.get("task_notes")
                    job.user = request.user
                    job.user.profile.uid = out.get("user_id", "")

                    job.save()
                    job.user.profile.save(update_fields=["uid"])

                except Exception as e:
                    print(e)
        return JsonResponse({"msg": "Submitted Successfully!"}, status=200)
    pass


@login_required
def view_job(request, job_id):
    template = loader.get_template('job/job.html')
    parents = accountmodels.Algorithm.objects.filter(
        parent_id=None, deleted=False).values().order_by("id")

    job = Job.objects.get(id=job_id)

    api = Api(token=request.session['bearer_token'])
    currentjob = api.get_execution(job.uid)

    styles = get_styles()
    exec_script = job.script
    algo = accountmodels.Algorithm.objects.get(
        scripts__execution_script=exec_script)
    bands = [{"name": currentjob["results"]["bands"][i]["name"],
              "index": i,
              "styles": styles[currentjob["results"]["bands"][i]["name"]]}
             for i in range(len(currentjob["results"]["bands"])) if currentjob["results"]["bands"][i]["add_to_map"]]
    context = {
        "parents":  views.get_algorithms(),
        "id": algo.parent.id,
        "bands": bands,
        "urls": currentjob["results"]["urls"]
    }
    return HttpResponse(template.render(context, request))


@login_required
def ajax_load_jobs(request, script_id):
    template = loader.get_template('job/task_tbl.html')
    context = {
        "jobs": getjobs(request, script_id)
    }
    return HttpResponse(template.render(context, request))


@login_required
def ajax_load_results(request, script_id):
    template = loader.get_template('job/jobs.html')
    context = {
        "jobs": getjobs(request, script_id)
    }
    return HttpResponse(template.render(context, request))


@login_required
def ajax_download_job(request, id):
    job = Job.objects.get(user=request.user, id=id, deleted=False)
    urls = job.results["urls"]
    print(urls)
    if len(urls) == 1:
        if url_exists(urls[0]["url"]):
            return JsonResponse({"url": urls[0]["url"]}, status=200)
        else:
            return JsonResponse({"msg": "Cannot download the results for this job!"}, status=400)

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
        return JsonResponse(
            {
                "msg": "Cannot download the results for this job"},
            status=400)


@login_required
def ajax_cancel_job(request, id):
    jobs = Job.objects.filter(user=request.user, id=id, deleted=False)
    for job in jobs:
        job.status = Status.objects.get(code="CANCELLED")
        job.save(update_fields=['status'])
    # api = Api(token=request.session['bearer_token'])
    template = loader.get_template('job/task_tbl.html')
    context = {
        "jobs": getjobs(request, jobs.first().script.id)
    }
    return HttpResponse(template.render(context, request))


@login_required
def ajax_delete_job(request, id):
    try:
        job = Job.objects.get(user=request.user, id=id, deleted=False)
        job.deleted = True
        job.status = Status.objects.get(code="DELETED")
        job.save(update_fields=['deleted', 'status'])
        template = loader.get_template('job/task_tbl.html')
        context = {
            "jobs": getjobs(request, job.script.id)
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print(e)
        return JsonResponse({"msg": "Job not found"}, status=400)


def getjobs(request, script_id):
    jobs = Job.objects.filter(
        user=request.user, script_id=script_id,
        deleted=False).order_by("-start_date")

    if not request.session.get('bearer_token'):
        views.signout(request)

    api = Api(token=request.session['bearer_token'])
    job_result = []
    for job in jobs:
        if job.status.value in ("PENDING", "RUNNING", "READY"):
            currentjob = api.get_execution(job.uid)
            if currentjob is not None:
                job.progress = currentjob["progress"]
                job.end_date = currentjob["end_date"]
                job.status = Status.objects.get(code=currentjob["status"])
                job.results = currentjob["results"]
                job.save(update_fields=["progress",
                                        "end_date", "status", "results"])
        job_result.append(job)
    return job_result
