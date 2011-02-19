# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_by_name, LEXERS
from taggit.managers import TaggableManager

ADDED_VIA = (
    ('web', 'Web'),
    ('firefox', 'Firefox'),
    ('komodo', 'Komodo'),
    ('netbeans', 'Netbeans'),
    ('eclipse', 'Eclipse'),
    ('unknown', 'Unknown'),
)

PRIVACY_CHOICES = (
    ('public', 'Public'),
    ('private', 'Private')
)

STATUS_CHOICES = (
    ('published', 'Published'),
    ('unpublished', 'Unplublished')
)

def _lexer_names():
    ret = []
    for lexer in LEXERS.itervalues():
        ret.append((lexer[2][0], lexer[1]))
    ret.sort()
    return tuple(ret)

class Snippet(models.Model):
    """A snippet with author and body"""

    author = models.ForeignKey(User)
    title = models.CharField(max_length=200,
                             help_text='Ex. Django URL middleware')
    description = models.TextField(blank = True,
                                help_text='Short description of your snippet')
    lexer = models.CharField(max_length=50, blank=True,
                             choices = (_lexer_names()),
        help_text = 'Choose one language or let snippify find it for you'
    )
    body = models.TextField(help_text="Snippet code goes here")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(blank = True, null=True)
    status = models.CharField(max_length = 50, default='published',
                              choices = STATUS_CHOICES)
    privacy = models.CharField(max_length=50, default='public',
                               choices=PRIVACY_CHOICES)

    tags = TaggableManager()
    # Used to provide some kind of stats
    via = models.CharField(max_length=50, default='web', choices=ADDED_VIA)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('snippets_read', [self.pk], )

    class Meta:
        ordering = ['-created_date']

    def highlight(self, body='', lexer = None, style="friendly"):
        """ Parse a piece of text and hightlight it as html"""
        if not lexer:
            lexer = get_lexer_by_name(u'text')
        return highlight(body, lexer, HtmlFormatter(style=style,
                                                    cssclass='source'))

class SnippetComment(models.Model):
    """ Django comment framework sucks! """

    snippet = models.ForeignKey(Snippet)
    user = models.ForeignKey(User)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']

class SnippetVersion(models.Model):
    """ History for snippets! """

    snippet = models.ForeignKey(Snippet)
    version = models.IntegerField(default=1)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-version']
