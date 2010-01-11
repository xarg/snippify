from django.template import RequestContext, loader, Context
from django.http import HttpResponse
import simplejson
import os

def build_context(request, extra_context=None):
	if extra_context is None:
		extra_context = {}
	if 'flash' in request.session:
		extra_context['flash']= request.session['flash']
		del request.session['flash']
	context = RequestContext(request)
	for key, value in extra_context.items():
		context[key] = callable(value) and value() or value
	return context
def lock(dir = '/tmp/snippify.lock'):
	try:
		os.mkdir(dir)
		return True
	except:
		return False
def unlock(dir = '/tmp/snippify.lock'):
	os.rmdir(dir)
class JsonResponse(HttpResponse):
	""" Broken """
	def __init__(self, data):
		content = simplejson.dumps(data,indent=2, ensure_ascii=False)
		super(JsonResponse, self).__init__(content=content, mimetype='application/json; charset=utf8')