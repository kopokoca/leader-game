from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^rules$', views.rules, name='rules'),
    url(r'^news$', views.post_list, name='post_list'),
    url(r'^news/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^news/new/$', views.post_new, name='post_new'),
    url(r'^news/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^news/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^news/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    #url(r'^user/detail/(?P<user_id>\d+)$', views.profile_detail, name='profile_detail'),
    url(r'^user/profile$', views.profile_detail,  name='profile_detail'),
    url(r'^rating$', views.rate_list,  name='rate_list'),
    url(r'^games/new$', views.game_new,  name='game_new'),
    url(r'^games/(?P<pk>\d+)/remove$', views.game_remove,  name='game_remove'),
    url(r'^games/(?P<pk>\d+)/add$', views.add_player,  name='add_player'),
    url(r'^games/(?P<pk>\d+)/play$', views.game_playing,  name='game_playing'),
]