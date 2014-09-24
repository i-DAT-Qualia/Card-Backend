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
    
    url(r'^api/v1/location/(?P<id>\d+)/totals/', 'cards.api.return_data.return_loc_totals'),

    (r'^api/', include(v1_api.urls)),
    url(r'api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),

    url(r'^api/cards/collector/', 'cards.api.collector.collect_scan'),

    url(r'^daystats/', 'cards.views.scan_weekends'),
    url(r'^averages/', 'cards.views.averages'),
    url(r'^upload/', 'cards.views.upload_scans'),


)
