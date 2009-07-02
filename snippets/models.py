from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from snippify.tags.models import Tag
from snippify.directories.models import Directory
from snippify.types.UUIDField import UUIDField

class Snippet(models.Model):
    """ 
        A snippet has one directory and many tags
        @todo: Should enable pygments + comments + versions
    """
    uuid = UUIDField(primary_key = True);
    tags = models.ManyToManyRel(Tag)
    directory = models.ForeignKey(Directory)    
    owner = models.ForeignKey(User)
       
    title = models.CharField(max_length = 200, blank = True)
    description = models.TextField(blank = True)
    body = models.TextField()
    created_date = models.DateTimeField(default = datetime.now())   
    updated_date = models.DateTimeField(blank = True, null=True)
    status = models.CharField(max_length = 200, default = 'published', choices = (('published', 'Published'),
                                                                                  ('unpublished', 'Unplublished')
                                                                                  ))
    privacy = models.CharField(max_length = 200, default = 'public', choices = (
                                                                                ('public', 'Public'),
                                                                                ('private', 'Private')
                                                                                ))
    def __unicode__(self): return self.title
    
    class Meta:
        ordering = ['-created_date', 'title']