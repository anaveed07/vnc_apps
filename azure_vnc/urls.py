from django.conf.urls import url
from wtools2.apps.vnc_console.azure_vnc.index import *

urlpatterns = \
    [
    url(r'^index/$', index.as_view(), name='index'),

]