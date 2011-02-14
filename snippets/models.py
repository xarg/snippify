from django.db import models
from django.contrib.auth.models import User

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_by_name, LEXERS

from taggit.managers import TaggableManager
#from tagging.fields import TagField
#from tagging.models import Tag

ADDED_VIA = (
    ('web', 'Web'),
    ('firefox', 'Firefox'),
    ('komodo', 'Komodo'),
    ('netbeans', 'Netbeans'),
    ('eclipse', 'Eclipse'),
    ('unknown', 'Unknown'),
)

# Search
#from djapian import space, Indexer

#Other
from datetime import datetime

def _lexer_names():
    ret = []
    for lexer in LEXERS.itervalues():
        ret.append((lexer[2][0], lexer[1]))
    ret.sort()
    return tuple(ret)

class Snippet(models.Model):
    """
        A snippet has one directory and many tags
        @todo: comments
        @todo: versions
        @todo: pygments + autodiscovery
    """
    author = models.ForeignKey(User)
    title = models.CharField(max_length = 200, help_text = 'Ex. Django URL middleware')
    description = models.TextField(blank = True, help_text = 'Short description of your snippet')
    lexer = models.CharField(
        max_length = 50,
        blank = True,
        choices = (_lexer_names()),
        help_text = 'Choose one language or let snippify find it for you'
    )
    body = models.TextField(help_text="Snippet code goes here")
    created_date = models.DateTimeField(default = datetime.now())
    updated_date = models.DateTimeField(blank = True, null=True)
    status = models.CharField(
        max_length = 50,
        default = 'published',
        choices = (
            ('published', 'Published'),
            ('unpublished', 'Unplublished')
        )
    )
    privacy = models.CharField(
        max_length = 50,
        default = 'public',
        choices = (
            ('public', 'Public'),
            ('private', 'Private')
        )
    )
    tags = TaggableManager()
    # Used to provide some kind of stats
    via = models.CharField(max_length=50,
                           default='web',
                           choices=ADDED_VIA)

    def __unicode__(self):
        return self.title

    def highlight(self, body = '', lexer = None):
        """ Parse a piece of text and hightlight it as html"""
        if not lexer:
            lexer = get_lexer_by_name(u'text')
        return highlight (body, lexer, HtmlFormatter(cssclass = 'source') )

    #@models.permalink
    def get_absolute_url(self):
        return '/' + str(self.pk)

    class Meta:
        ordering = ['-created_date']

class SnippetComment(models.Model):
    """ Django comment framework sucks! """

    snippet = models.ForeignKey(Snippet)
    user = models.ForeignKey(User)
    body = models.TextField()
    created_date = models.DateTimeField(default=datetime.now())
    class Meta:
        ordering = ['created_date']

class SnippetVersion(models.Model):
    """ History for snippets! """

    snippet = models.ForeignKey(Snippet)
    version = models.IntegerField(default = 1)
    body = models.TextField()
    created_date = models.DateTimeField(default=datetime.now())
    class Meta:
        ordering = ['-version']


#class SnippetIndexer(Indexer):
#    """ Used by djapian """
#    fields = ['title', 'description', 'body', 'tags', 'lexer']
#    tags = [
#        ('author', 'author'),
#        ('pk', 'pk'),
#        ('created_date', 'created_date')
#    ]
#class TagIndexer(Indexer):
#    """ Used by djapian """
#    fields = ['name']
#    tags = [
#        ('name', 'name')
#    ]
#space.add_index(Snippet, SnippetIndexer, attach_as='indexer')
#space.add_index(Tag, TagIndexer, attach_as='indexer')
