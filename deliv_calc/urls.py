from django.conf.urls import patterns, url

from deliv_calc import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
