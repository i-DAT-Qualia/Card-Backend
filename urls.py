from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from cards.api.resources import *

from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(BatchResource())
v1_api.register(CardResource())
v1_api.register(ReaderResource())
v1_api.register(LocationResource())
v1_api.register(ReaderLocationResource())
v1_api.register(ScanResource())

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    

    (r'^api/', include(v1_api.urls)),
    url(r'api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),

    url(r'^api/cards/collector/', 'cards.api.collector.collect_scan'),

)
