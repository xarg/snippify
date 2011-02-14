from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^profile/', views.view_profile, name='accounts_profile'),
    url(r'^edit/', views.edit, name='accounts_edit'),
    url(r'^follow/(\w+)/?', views.follow, name='accounts_follow'),
    url(r'^unfollow/(\w+)/?', views.unfollow, name='accounts_unfollow'),
    url(r'^followers/(\w+)/?', views.followers, name='accounts_followers'),
    url(r'^following/(\w+)/?',views.following, name='accounts_following'),
    url(r'^refresh_key/?', views.refresh_key, name='accounts_refresh_key'),
    url(r'^unsubscribe/?',views.unsubscribe, name='accounts_unsubscribe'),
    url(r'^(\w+)/',views.user, name='accounts_user'),
)
