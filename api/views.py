from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from snippify.snippets.models import Snippet
from django_authopenid.models import UserProfile
from django.contrib.auth.models import User

from pygments.lexers import guess_lexer, LEXERS
from pygments.util import ClassNotFound

from logging import debug
import simplejson

def _auth(request):
	key = request.META.get('HTTP_RESTKEY', None)
	if key:
		try:
			profile = UserProfile.objects.get(restkey=key)
			return User.objects.get(pk=profile.user.pk)
		except:
			return None
	else:
		return None
@csrf_exempt
def create(request):
	""" Expect a post """
	user = _auth(request)
	if user:
		data = simplejson.loads(request.POST.get('data', ''))
		try:
			lexer_obj = guess_lexer(body)
			for lex in LEXERS.itervalues():
				if lexer_obj.name == lex[1]:
					lexer = lex[2][0].lower()
					break
		except ClassNotFound:
			lexer = u'text'
		try:
			snippet = Snippet(author=user, title=data['title'] , description=data['description'] , body=data['body'], tags=data['tags'], lexer=lexer)
			snippet.save()
			return HttpResponse('SUCCESS')
		except:
			return HttpResponse('VALIDATION')
	else:
		return HttpResponse('AUTH')