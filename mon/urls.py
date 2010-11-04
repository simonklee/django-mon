from django.conf.urls.defaults import *

urlpatterns = patterns('mon.views',
    url(r'^(?P<pattern>.+)?$', 'mon_router', name = 'mon_router'),
)
