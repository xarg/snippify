from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',    
    (r'^home$', 'snippify.snippets.views.index'), # The dashboard. Latest news/snippets whatever related to snippets. (Friend snippets)
    (r'^snippets/(my)$', 'snippify.snippets.views.my'),# Just a list of your snippets
    (r'^(\d+)$', 'snippify.snippets.views.read'), #View some snippet Ex: /11233 
    
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