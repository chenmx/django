from django.conf.urls import patterns, url

from tinoauths import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^active/', views.active, name='active'),
        # url(r'^search/$', views.search, name='search'),
)
