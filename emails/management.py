from django.db.models import signals

# Models
from snippify.snippets.models import Snippet
from django.contrib.comments.models import Comment
from snippify.django_authopenid.models import UserFollow
from snippify.emails.models import EmailQueue

from django.shortcuts import render_to_response
def post_save_snippet(sender, **kwargs):
	"""
	Send notifications to users that follow the snippet creator
	"""
	queue = EmailQueue()
	queue.save()
	
def post_save_follow(sender, **kwargs):
	"""
	User started following another user - send notification
	"""
	pass
def post_save_comment(sender, **kwargs):
	"""
	User commented a snippet - send notification
	"""
	pass

signals.post_save.connect(post_save_snippet, sender=Snippet)
signals.post_save.connect(post_save_follow, sender=UserFollow)
signals.post_save.connect(post_save_comment, sender=Comment)