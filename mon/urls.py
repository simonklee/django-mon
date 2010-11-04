from django.conf.urls.defaults import *
from piston.resource import Resource

from mon.handlers import MonHandler

mon = Resource(handler=MonHandler)

urlpatterns = patterns('',
    url(r'^(?P<pattern>.+)?$', mon, name = 'mon_router'),
    url(r'^(?P<pattern>.+)?\.(?P<emitter_format>.+)$', mon, name = 'mon_router'),
)
