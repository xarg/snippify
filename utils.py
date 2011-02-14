import json
import os

from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.utils.datastructures import SortedDict

def build_context(request, extra_context = {}):
    """ Add flash message from session, and add some custom vars via
    extra_context"""
    extra_context['current_path'] = request.get_full_path()

    if 'flash' in extra_context:
        del extra_context['flash']
    if 'flash' in request.session:
        extra_context['flash'] = request.session['flash']
        del request.session['flash']

    context = RequestContext(request)

    for key, value in extra_context.items():
        context[key] =  value() if callable(value) else value
    return context

def order_fields(fields, order=[]):
    """Used to reorder fields in forms
    Args:

    fields -- SortedDict fields property
    order -- List/tuple of the order

    """
    order.extend(fields.keys())
    ordered_fields = SortedDict()
    for item in order:
        ordered_fields[item] = fields[item]
    return ordered_fields

class JsonResponse(HttpResponse):
    """ Broken """
    def __init__(self, data):
        content = json.dumps(data,indent=2, ensure_ascii=False)
        super(JsonResponse, self).__init__(content=content,
                                    mimetype='application/json; charset=utf8')
