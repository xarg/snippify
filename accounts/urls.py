from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^profile/', views.profile),
    url(r'^edit/', views.edit),
    url(r'^follow/(\w+)/?', views.follow),
    url(r'^unfollow/(\w+)/?', views.unfollow),
    url(r'^followers/(\w+)/?', views.followers),
    url(r'^following/(\w+)/?',views.following),
    url(r'^refresh_key/?', views.refresh_key),
    url(r'^unsubscribe/?',views.unsubscribe),
    url(r'^(\w+)/',views.user),
)
