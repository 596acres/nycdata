from django.conf.urls import patterns, url

from .views import NYCHAGeoJSONListView


urlpatterns = patterns('',
    url(r'^$', NYCHAGeoJSONListView.as_view(), name='nycha_list'),
)
