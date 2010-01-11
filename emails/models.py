from django.db import models
from django.conf import settings

#Other
from datetime import datetime

class EmailQueue(models.Model):
	mail_to = models.CharField(max_length = 200)
	mail_from = models.CharField(max_length = 200, default=settings.DEFAULT_FROM_EMAIL)
	mail_replyto = models.CharField(max_length = 200, default=settings.DEFAULT_REPLYTO_EMAIL)
	mail_subject = models.CharField(max_length = 200)
	mail_body = models.TextField()
	created_date = models.DateTimeField(default = datetime.now())