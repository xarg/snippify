# -*- coding: utf-8 -*-
""" API views. Do stuff with **snippify.snippets.models.Snippet**

"""
import json

from pygments.lexers import guess_lexer, LEXERS
from pygments.util import ClassNotFound

from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from snippify.accounts.models import UserProfile

from models import Snippet
from forms import SnippetCreateForm

def auth(view):
    def decorator(request):
        key = request.META.get('HTTP_RESTKEY', None)
        if key:
            try:
                profile = UserProfile.objects.get(restkey=key)
                login(request, User.objects.get(pk=profile.user.pk))
            except UserProfile.DoesNotExist:
                return HttpResponse('NOT_AUTHORIZED')
        else:
            return HttpResponse('NOT_AUTHORIZED')
    return decorator

@csrf_exempt
@auth
def create(request):
    """ Create a snippet """

    data = json.loads(request.POST.get('data', '{}'))
    form = SnippetCreateForm(data)

    if not form.is_valid():
        return HttpResponse('VALIDATION')
    try:
        lexer_obj = guess_lexer(data['body'])
        for lex in LEXERS.itervalues():
            if lexer_obj.name == lex[1]:
                lexer = lex[2][0].lower()
                break
    except ClassNotFound:
        lexer = u'text'
    try:
        snippet = Snippet(
            author = user,
            title = data['title'],
            description = data['description'],
            body=data['body'],
            lexer=lexer,
            via=data['via'],
            privacy = data['privacy'],
            status = data['status']
        )
        snippet.save()
        snippet.tags = data['tags']
        snippet.save_m2m()

        return HttpResponse('SUCCESS')
    except Exception, e:
        return HttpResponse('ERROR: %s' % str(e))
