from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^snippets$', 'snippify.snippets.views.index'),# A list of your snippets
    (r'^([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$', 'snippify.snippets.views.read'), #View snippet UUID Ex: /9b4cd7a8-6741-11de-a251-8f06b6bf0ee7
    (r'^edit/([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$', 'snippify.snippets.views.edit'), #Edit snippet
    (r'^delete/([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$', 'snippify.snippets.views.delete'), #Delete snippet 
    
    (r'^tags$', 'snippify.tags.views.index'), # View all tags in a tag could
    (r'^tags/(my)$', 'snippify.tags.views.my'), # View your tags    
    (r'^tag/(.*)$', 'snippify.tags.views.read'), # View snippets from this tag from others. Ex: tag/python
    
    (r'^dirs/([^my]+)$', 'snippify.directories.views.index'), # Display some users directories 
    (r'^dirs/(my)$', 'snippify.directories.views.my'), # Display your directories
    (r'^dir/(.*)$', 'snippify.directories.views.read'), # Display some directory
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
   (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/?(.*)', admin.site.root),
    
    (r'^/?$', 'snippify.pages.views.index'), # Match /
    (r'^(.*)$', 'snippify.pages.views.read') #  Match everything else and pass it to Page
)