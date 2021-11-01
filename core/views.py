from json.encoder import JSONEncoder
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse
)
from django.shortcuts import render
from django.template import loader
from account import models
from utils.util import matrix_to_table, table_to_matrix
# Create your views here.


def dashboard(request):
    template = loader.get_template('core/index.html')
    parents = models.Algorithm.objects.filter(parent_id=None).values()
    algorithms = []
    for parent in parents:
        children = models.Algorithm.objects.filter(
            parent_id=parent['id'], uid=None)
        if children.count() > 0:
            parent["children"] = children
        algorithms.append(parent)
    context = {
        "parents": algorithms
    }
    return HttpResponse(template.render(context, request))


def view_algorithm(request, algo_id):
    template = loader.get_template('core/algorithm.html')
    parents = models.Algorithm.objects.filter(parent_id=None).values()
    algorithms = []
    for parent in parents:
        children = models.Algorithm.objects.filter(
            parent_id=parent['id'], uid=None)
        if children.count() > 0:
            parent["children"] = children
        algorithms.append(parent)
    context = {
        "parents":  algorithms,
        "children":  models.Algorithm.objects.filter(parent_id=algo_id),
        "id": algo_id,
        "table": matrix_to_table()
    }
    return HttpResponse(template.render(context, request))


def ajax_get_runmode(request, id):
    scripts = models.Algorithm.objects.get(id=id).scripts.all()
    runmodes = []
    options = ""
    for script in scripts:
        runmode = script.execution_script.run_mode
        runmodes.append({"id": runmode.id, "value":  runmode.value})
        options += "<option value='{}'>{}</option>".format(
            runmode.id, runmode.value)
    return JsonResponse({"runmodes": runmodes, "options": options})


def ajax_get_algorithm_view(request, id, runmode):
    if runmode < 1:
        script = models.ExecutionScript.objects.filter(
            script__in=[obj.id for obj in models.Script.objects.filter(
                algorithm__id=id)])
    else:
        script = models.ExecutionScript.objects.filter(
            run_mode_id=runmode,
            script__in=[obj.id for obj in models.Script.objects.filter(
                algorithm__id=id)])
    if script.count() > 0:
        return render(request, 'core/forms/' + script.first().name + ".html",
                      {"table": matrix_to_table()})
