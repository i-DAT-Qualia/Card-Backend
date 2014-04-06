from tastypie.resources import ModelResource
from tastypie import fields
from tastypie import utils
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.validation import Validation, FormValidation
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from cards.models import *

from tastypie.authentication import Authentication
from tastypie.http import HttpUnauthorized


class KeyOnlyAuthentication(Authentication):
    '''
    Authorises API calls using just the API Key - Likely not perfect,
    but reduces complexity for end developer.
    '''
    def _unauthorized(self):
        return HttpUnauthorized()

    def is_authenticated(self, request, **kwargs):
        from tastypie.models import ApiKey

        try:
            key = ApiKey.objects.get(key=request.GET.get('api_key') or request.POST.get('api_key'))
            request.user = key.user
        except ApiKey.DoesNotExist:
            return self._unauthorized()

        return True


class BatchResource(ModelResource):
    class Meta:
        queryset = Batch.objects.all()
        authentication = KeyOnlyAuthentication()
        resource_name = 'batch'
        allowed_methods = ['get','post','put','patch']
        always_return_data = True


class CardResource(ModelResource):
    scans = fields.ToManyField('cards.api.resources.ScanResource', 'scan_set', full=True, null=True)
    batch = fields.ToOneField('cards.api.resources.BatchResource', 'batch', null=True, full=True)

    class Meta:
        queryset = Card.objects.all()
        authentication = KeyOnlyAuthentication()
        resource_name = 'card'
        allowed_methods = ['get','post','put','patch']
        always_return_data = True
        filtering = {
            'code': ALL
        }


class ReaderResource(ModelResource):
    class Meta:
        queryset = Reader.objects.all()
        authentication = KeyOnlyAuthentication()
        resource_name = 'reader'
        allowed_methods = ['get','post','put','patch']
        always_return_data = True


class LocationResource(ModelResource):
    class Meta:
        queryset = Location.objects.all()
        authentication = KeyOnlyAuthentication()
        resource_name = 'location'
        allowed_methods = ['get','post','put','patch']
        always_return_data = True


class ReaderLocationResource(ModelResource):
    reader = fields.ToOneField('cards.api.resources.ReaderResource', 'reader', full=True)
    location = fields.ToOneField('cards.api.resources.LocationResource', 'location', full=True)

    class Meta:
        queryset = ReaderLocation.objects.all()
        authentication = KeyOnlyAuthentication()
        resource_name = 'readerlocation'
        allowed_methods = ['get','post','put','patch']
        always_return_data = True


class ScanResource(ModelResource):
    readerLocation = fields.ToOneField('cards.api.resources.ReaderLocationResource', 'readerLocation', full=True, null=True)
    card = fields.ToOneField('cards.api.resources.CardResource', 'card', null=True)

    class Meta:
        queryset = Scan.objects.all()
        authentication = KeyOnlyAuthentication()
        resource_name = 'scan'
        allowed_methods = ['get','post','put','patch']
        always_return_data = True
