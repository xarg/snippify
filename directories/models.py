from django.db import models
from django.contrib.auth.models import User

class Directory (models.Model):
    """ A directory has many snippets """
    DEFAULT_DIRNAME = 'Archive'
    title = models.TextField(default = DEFAULT_DIRNAME)
    weight = models.IntegerField(max_length = 5)
    owner = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ['-weight', 'title']