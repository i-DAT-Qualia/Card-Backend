from cards.models import *

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response

from django.views.decorators.csrf import csrf_exempt

from datetime import datetime

from tastypie.models import ApiKey

import json

#custom method for collecting gps data
@csrf_exempt
def collect_scan(request):
    success = False
    
    #check for a key
    if request.GET.get("api_key"):

        try:
            key = ApiKey.objects.get(key=request.GET.get('api_key'))

            if request.method == "POST":
                data = json.loads(request.body)

                the_card, created = Card.objects.get_or_create(
                    code=data['code']
                )

                the_readerLocation = ReaderLocation.objects.filter(
                    reader__id=data['reader']
                ).latest('updated')
                

                the_scan = Scan()
                the_scan.card = the_card
                the_scan.readerLocation = the_readerLocation
                the_scan.added = datetime.strptime(data['datetime'], '%d%m%Y%H%M%S')

                the_scan.save()

                success = True

        except ApiKey.DoesNotExist:
            success = "Error - ApiKey DoesNotExist"

    return render_to_response('success.json', {
        'success': success,
    }, context_instance=RequestContext(request))
