from django.conf.urls.defaults import *
from piston.resource import Resource

from mon.handlers import MonHandler

mon = Resource(handler=MonHandler)

urlpatterns = patterns('mon.views',
    url(r'^(?P<pattern>.+)?$', mon, name = 'mon_router'),
)
