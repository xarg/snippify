from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'snippify.pages.views.index'),
    (r'^page/(.*)$', 'snippify.pages.views.read'),
    
    (r'^snippets$', 'snippify.snippets.views.index'), # View latest snippets from your friends or yourself
    (r'^(\d+)$', 'snippify.snippets.views.read'), #View some snippet Ex: /292934
    
    (r'^tag/(.*)$', 'snippify.tags.views.index'), #View snippets from this tag and others. Ex: tag/python
    (r'^dir/(.*)$', 'snippify.directories.views.index'), #Display some directory
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
   (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
