from django.db import models

class Tag (models.Model):
    """ A tag has many snippets """
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']