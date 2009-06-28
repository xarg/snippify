from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

class Page(models.Model):
    """ This model is used for serving static pages such as about/TOS etc.."""
    title = models.CharField(max_length=200, primary_key=True)
    body = models.TextField(blank = True)
    author = models.ForeignKey(User)
    date_created = models.DateField(default = datetime.now())
    date_updated = models.DateField(blank = True)
    
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ['-date_updated', '-date_created']