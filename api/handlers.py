# PISTON DOESN'T SUPPORT CSRF BYPASS - FUCK IT
from django import forms
from django.http import HttpRequest

from piston.handler import BaseHandler
from piston.utils import throttle, validate

from django_authopenid.models import UserProfile
from snippify.snippets.models import Snippet

from logging import debug, log

class SnippetForm(forms.ModelForm):
	class Meta:
		model = Snippet

class SnippetHandler(BaseHandler):
	allowed_methods = ('POST',)
	model = Snippet

	#@validate(SnippetForm)
	#@throttle (5, 10*60)
	def create(self, request):
		title = request.POST.get('title', '')
		description = request.POST.get('description', '')
		body = request.POST.get('body', '')
		tags = request.POST.get('tags', '')
		lexer = 'text'
		return Snippet(title=title, description=description, body=body, tags=tags, lexer=lexer)
class HttpBasicAuthentication(object):
	"""
		Authenficate by restkey from UserProfile
	"""
	def __init__(self):
		pass
	def is_authenticated(self, request):
		"""
		This method call the `is_authenticated` method of django
		User in django.contrib.auth.models.

		`is_authenticated`: Will be called when checking for
		authentication. It returns True if the user is authenticated
		False otherwise.
		"""

		self.request = request
		try:
			UserProfile.objects.get(restkey=request.POST.get('RESTKEY'))
			return True
		except:
			return False
	def challenge(self):
		resp = HttpResponse("Authorization Required")
		resp['WWW-Authenticate'] = 'Basic realm="API"'
		resp.status_code = 401
		return resp