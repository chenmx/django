from django.conf.urls import patterns, url

from ads import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^ads$', views.get_ads, name='get_ads'),
        url(r'^click$', views.click, name='click'),
)
