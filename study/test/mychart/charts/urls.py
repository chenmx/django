from django.conf.urls import patterns, url

from charts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^weather/$', views.weather_chart_view, name='weather_chart_view'),
)
