from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from logging import debug

from snippify.pages.models import Page #@PydevCodeAnalysisIgnore

def index(request):
    p = get_object_or_404(Page, pk='Front')
    return render_to_response('pages/index.html')
def read(request, page_title):
    """ Return a certain page """
    p = get_object_or_404(Page, pk=page_title)
    return render_to_response('pages/page.html', {'page': p})