from django.conf.urls.defaults import *
from snippify.feeds import LatestSnippets, LatestTag, LatestUser
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

feeds = {
	'latest': LatestSnippets,
	'tag' : LatestTag,
	'user' : LatestUser
}

#Load search index
import djapian
djapian.load_indexes()

#Django piston - doesn't work with CSRF
#from piston.resource import Resource
#from snippify.api.handlers import SnippetHandler, HttpBasicAuthentication
#snippet_handler = Resource(SnippetHandler)

urlpatterns = patterns('',
	(r'^/?$', 'snippify.pages.views.index'),

	(r'^snippets/?$', 'snippify.snippets.views.index'),
	(r'^(\d+)/?$', 'snippify.snippets.views.read'),
	(r'^create/?$', 'snippify.snippets.views.create'),
	(r'^update/(\d+)/?$', 'snippify.snippets.views.update'),
	(r'^delete/(\d+)/?$', 'snippify.snippets.views.delete'),
	(r'^download/(\d+)/?$', 'snippify.snippets.views.download'),
	(r'^history/(\d+)/?$', 'snippify.snippets.views.history'),
	(r'^comment/(\d+)/?$', 'snippify.snippets.views.comment'),
	(r'^search/?$', 'snippify.snippets.views.search'),


	(r'^account/', include('django_authopenid.urls')),
	(r'^accounts/profile/','snippify.accounts.views.profile'),
	(r'^accounts/edit/','snippify.accounts.views.edit'),
	(r'^accounts/follow/(\w+)/?','snippify.accounts.views.follow'),
	(r'^accounts/unfollow/(\w+)/?','snippify.accounts.views.unfollow'),
	(r'^accounts/followers/(\w+)/?','snippify.accounts.views.followers'),
	(r'^accounts/following/(\w+)/?','snippify.accounts.views.following'),
	(r'^accounts/refresh_key/?','snippify.accounts.views.refresh_key'),
	(r'^accounts/unsubscribe/?','snippify.accounts.views.unsubscribe'),
	(r'^accounts/(\w+)/','snippify.accounts.views.user'),

	(r'^tag/(?P<tag>[^/]+)/?$', 'snippify.tags.views.view'),
	(r'^tag/(?P<tag>[^/]+)/(?P<username>[^/]+)/?$', 'snippify.tags.views.user'),
	(r'^tags/?$', 'snippify.tags.views.index'),

	(r'^api/snippet/create/?$', 'snippify.api.views.create'),

	(r'^feeds/(?P<url>.*)/?$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
	(r'^admin/', include(admin.site.urls)),
)