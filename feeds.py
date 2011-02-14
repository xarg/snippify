"""
@todo: Set site name in the text fields
"""
from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist

# Models
from snippets.models import Snippet
from tagging.models import Tag, TaggedItem
from django.contrib.auth.models import User
# Misc
# from logging import debug

class LatestSnippets(Feed):
    title = "Latest snippets"
    link = "/snippets/"
    description = "Updates on changes and additions to snippify.me"
    
    def items(self):
        return Snippet.objects.order_by('-created_date')[:10]

class LatestTag(Feed):
    """ Get latest snippets from a specific tag"""    
    def get_object(self, bits):
        if len(bits) != 2:
            raise ObjectDoesNotExist
        tag = Tag.objects.get(name=bits[0])
        if tag is None:
            raise FeedDoesNotExist
        return tag
    def title(self, obj):
        return "Latest snippets in %s" % obj.name
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return '/tag/' + str(obj.name) + '/'
    def description(self, obj):
        return "Updates on changes and additions to snippify.me in %s tag" % obj.name        
    def items(self, obj):        
        return TaggedItem.objects.get_by_model(Snippet, obj).order_by('-created_date')[:10]       
class LatestUser(Feed):
    """ Get latest snippets from a specific user"""    
    def get_object(self, bits):
        if len(bits) != 2:
            raise ObjectDoesNotExist
        user = User.objects.get(username=bits[0])
        if user is None:
            raise FeedDoesNotExist
        return user
    def title(self, obj):
        return "Latest snippets in %s" % obj.username
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return '/account/' + str(obj.username) + '/'
    def description(self, obj):
        return "Updates on changes and additions to snippify.me in %s tag" % obj.username        
    def items(self, obj):        
        return Snippet.objects.filter(author=obj.id).order_by('-created_date')[:10]