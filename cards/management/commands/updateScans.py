from django.core.management.base import BaseCommand, CommandError
from cards.models import *
import datetime, math, time
from decimal import Decimal


def updater(reader_id,start_date,end_date,reader_location_id):
    scans = Scan.objects.filter(readerLocation__reader__id = reader_id)
    scans = scans.filter(added__range=[start_date, end_date])
    new_reader_location = ReaderLocation.objects.get(id=reader_location_id)

    for scan in scans:
        print scan
        scan.readerLocation = new_reader_location
        scan.save()
        print scan



class Command(BaseCommand):
    help = 'Updates scans to the correct location'
    
    
    def handle(self, *args, **options):
        print "Updating scans"

        #Use this if the scheduler fails

        updater('1', '2014-03-21', '2014-03-24','2')

