# Create your views here.
from django.conf import settings
from django.core.urlresolvers import reverse

from django.template import RequestContext, loader, Context
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect

from snippify.snippets.models import Snippet
from snippify.utils import build_context

#Other
from logging import debug

def index(request, extra_context=None):
	""" 
	This is the first page
	Need to return latest 10 snippets
	@todo: tag cloud
	"""
	snippets = Snippet.objects.all()[0:5]
	if snippets == None:
		snippets = []
	return render_to_response('pages/index.html', {'snippets': snippets, 'home_page': True }, 
							context_instance=build_context(request, extra_context=extra_context))  
