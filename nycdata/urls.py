from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
    url(r'^nycha/', include('nycdata.nycha.urls')),
)
