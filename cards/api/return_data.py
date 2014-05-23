from cards.models import *

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response

from django.views.decorators.csrf import csrf_exempt

from datetime import datetime

from tastypie.models import ApiKey

from django.core.exceptions import ObjectDoesNotExist

import json

def return_loc_totals(request, id):
    data = {}
    #check for a key
    if request.GET.get("api_key"):
        key = ApiKey.objects.get(key=request.GET.get('api_key'))

        scans = Scan.objects.filter(readerLocation__location__id=id)
        adults = scans.filter(card__is_child=False)
        children = scans.filter(card__is_child=True)

        unique_adults = scans.distinct('card')
        unique_children = scans.distinct('card')

        data['unique_adult'] = unique_adults.count()
        data['total_adult'] = adults.count()
        data['unique_child'] = unique_children.count()
        data['total_child'] = children.count()

    return HttpResponse(json.dumps(data), content_type="application/json")







