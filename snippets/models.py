from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from snippify.tags.models import Tag #@PydevCodeAnalysisIgnore

class Snippet(models.Model):
    """ A snippet has one directories and many tags """
    owner = models.ForeignKey(User)
    
    title = models.CharField(max_length = 200, blank = True)
    description = models.TextField(blank = True)
    body = models.TextField()
    created_date = models.DateTimeField(default = datetime.now())   
    updated_date = models.DateTimeField(blank = True)
    status = models.CharField(max_length = 200, default = 'published', choices = (
                                                                                  ('published', 'Published')
                                                                                  ('unpublished', 'Unplublished')
                                                                                  ))
    privacy = models.CharField(max_length = 200, default = 'public', choices = (
                                                                                ('public', 'Public')
                                                                                ('private', 'Private')
                                                                                ))
    tags = models.ManyToManyRel(Tag)