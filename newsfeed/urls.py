from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'newsfeed'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^news$', views.news_list, name='news'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^source/(?P<pk>[0-9]+)/$', views.SourceDetailView.as_view(), name='source-detail'),
    url(r'^subscribe/$', views.SourceListView.as_view(), name='subscribe'),
]
