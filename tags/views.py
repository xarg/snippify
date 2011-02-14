from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse

from snippify.snippets.models import Snippet
from snippify.utils import build_context

#from tagging.models import Tag, TaggedItem

#Other
from logging import debug

def index(request):
    tags = Tag.objects.all()
    return render_to_response('tags/index.html', {}, context_instance=build_context(request))
def view(request, tag = None):
    try:
        tag_object = Tag.objects.get(name=tag)
        snippets = TaggedItem.objects.get_by_model(Snippet, tag_object)
    except:
        snippets = None
    return render_to_response('tags/view.html', {'tag': tag, 'snippets': snippets}, context_instance=build_context(request))
def user(request, tag = None, username = None):
    try:
        tag_object = Tag.objects.get(name=tag)
        snippets = TaggedItem.objects.get_by_model(Snippet, tag_object)
    except:
        snippets = None
    return render_to_response('tags/view.html', {'tag': tag, 'snippets': snippets}, context_instance=build_context(request))
