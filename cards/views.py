from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import Context, loader, RequestContext

from cards.forms import UploadScansForm
from cards.models import *

from datetime import datetime

#import datetime

from tastypie.models import ApiKey

from django.core.exceptions import ObjectDoesNotExist

import json

import numpy


def handle_scans(scan_file):
    scans = json.load(scan_file)
    for scan in scans:

        the_scan = Scan()

        the_card, created = Card.objects.get_or_create(
            code=scan['code']
        )

        the_scan.card = the_card

        
        added = datetime.strptime(scan['datetime'], '%d%m%Y%H%M%S')
        
        if not added.year == 2001:
            the_scan.added = added 

            try:
                the_readerLocation = ReaderLocation.objects.filter(
                    reader__id=scan['reader'],
                #).latest('updated')
                ).get(start__lte=the_scan.added, end__gte=the_scan.added)

            except ObjectDoesNotExist:
                #if a card is scaned between opening dates, default to the old behavour.
                the_readerLocation = ReaderLocation.objects.filter(
                    reader__id=scan['reader'],
                ).latest('updated')

        else: 
            the_readerLocation = ReaderLocation.objects.filter(
                reader__id=scan['reader'],
            ).latest('updated')

        the_scan.readerLocation = the_readerLocation
        the_scan.save()

def upload_scans(request):
    success = False
    if request.GET.get("api_key"):

        try:
            key = ApiKey.objects.get(key=request.GET.get('api_key'))
            if request.method == 'POST':
                form = UploadScansForm(request.POST, request.FILES)
                if form.is_valid():
                    print request.FILES['scan_file']
                    handle_scans(request.FILES['scan_file'])
                    success = True
            else:
                form = UploadScansForm()
        except ApiKey.DoesNotExist:
            success = "Error - ApiKey DoesNotExist"

    return render_to_response('upload.html', 
        {'form': form, 'success':success, 'key':key.key},
        context_instance=RequestContext(request)
    )


def scan_weekends(request):

    return render_to_response('dates.html', {
        '11may': Scan.objects.filter(added__year='2014', added__month='05', added__day='11').count(), 
        '12may': Scan.objects.filter(added__year='2014', added__month='05', added__day='12').count(), 
        '8june': Scan.objects.filter(added__year='2014', added__month='06', added__day='08').count(),
        '9june': Scan.objects.filter(added__year='2014', added__month='06', added__day='09').count(),
        '13july': Scan.objects.filter(added__year='2014', added__month='07', added__day='13').count(),
        '14july': Scan.objects.filter(added__year='2014', added__month='07', added__day='14').count()
    },context_instance=RequestContext(request))


def averages(request):

    if request.GET.get("api_key"):

        try:
            key = ApiKey.objects.get(key=request.GET.get('api_key'))

            overall_scan_numbers = []
            child_scan_numbers = []
            adult_scan_numbers = []

            overall_max_scan = 0
            child_max_scan = 0
            adult_max_scan = 0

            for card in Card.objects.all():
                scans = Scan.objects.filter(card=card).exclude(readerLocation__location__id=1).count()
                if not scans == 0:
                    overall_scan_numbers.append(scans)

                    if scans > overall_max_scan:
                        overall_max_scan = scans

                    if card.is_child:
                        child_scan_numbers.append(scans)

                        if scans > child_max_scan:
                            child_max_scan = scans

                    else:
                        adult_scan_numbers.append(scans)

                        if scans > adult_max_scan:
                            adult_max_scan = scans

            overall_average = numpy.mean(overall_scan_numbers)
            child_average = numpy.mean(child_scan_numbers)
            adult_average = numpy.mean(adult_scan_numbers)

            batch_detail = []

            for batch in Batch.objects.all():
                batch_overall_scan_numbers = []
                batch_child_scan_numbers = []
                batch_adult_scan_numbers = []

                batch_child_total = 0
                batch_adult_total = 0

                for card in Card.objects.filter(batch=batch):
                    scans = Scan.objects.filter(card=card).exclude(readerLocation__location__id=1).count()
                    if not scans == 0:
                        batch_overall_scan_numbers.append(scans)


                        if card.is_child:
                            batch_child_scan_numbers.append(scans)
                            batch_child_total += 1
                        else:
                            batch_adult_scan_numbers.append(scans)
                            batch_adult_total += 1

                batch_detail.append({
                    'name':batch.name,
                    'overall_average': numpy.mean(batch_overall_scan_numbers),
                    'child_average': numpy.mean(batch_child_scan_numbers),
                    'adult_average': numpy.mean(batch_adult_scan_numbers),
                    'child_total': batch_child_total,
                    'adult_total': batch_adult_total
                })


            return render_to_response('averages.html', {
                'overall_average': overall_average,
                'child_average': child_average,
                'adult_average': adult_average,
                'overall_max_scan': overall_max_scan,
                'child_max_scan': child_max_scan,
                'adult_max_scan': adult_max_scan,
                'batches': batch_detail
            },context_instance=RequestContext(request))
            
            

        except ApiKey.DoesNotExist:
            error = "Error - API Key Does Not Exist"
        
    else:
        error = "Error - No API Key"        

    return render_to_response('averages.html', {
        'error': error,
    },context_instance=RequestContext(request))
