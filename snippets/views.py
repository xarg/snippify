# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from logging import debug

from snippify.snippets.models import Snippet #@PydevCodeAnalysisIgnore

def index(request):
    """ This is /home/ """
    #snippet = get_object_or_404(Snippet)
    #return render_to_response('snippets/index.html', {'snippet': snippet})
    pass
def my(request):
    """ List of my snippets """
    pass
def read(request, id):
    snippet = get_object_or_404(Snippet, pk=id)
    return render_to_response('snippets/read.html', {'snippet': snippet})

def edit(request, id):
    """ @todo: Check if is owner """
    snippet = get_object_or_404(Snippet, pk=id)
    return render_to_response('snippets/edit.html', {'snippet': snippet})

def delete(request, id):
    """ @todo: Check if is owner """
    snippet = get_object_or_404(Snippet, pk=id)
    return render_to_response('snippets/my.html', {'snippet': snippet})