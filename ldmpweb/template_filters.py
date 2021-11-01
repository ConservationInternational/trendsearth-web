import json
from django.template.defaulttags import register
from django.core.serializers import serialize
from django.db.models.query import QuerySet


@register.filter(name='get_item')
def get_item(value, arg):
    return value.get(arg)


@register.filter(name='jsonify')
def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return json.dumps(object)


@register.filter(name='range')
def filter_range(start, end):
    return range(start, end + 1)
