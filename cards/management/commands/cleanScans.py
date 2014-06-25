from django.core.management.base import BaseCommand, CommandError
from cards.models import *
import datetime, math, time
from decimal import Decimal


class Command(BaseCommand):
    help = 'Cleans Up Scans'
    
    
    def handle(self, *args, **options):
        now = datetime.datetime.now()
        delta = datetime.timedelta(hours=1)
        start = datetime.datetime(2014, 5, 1)

        for card in Card.objects.all():
            #print card
            scan_list = Scan.objects.filter(card=card)

            for loc in ReaderLocation.objects.all():
                #print loc
                filtered_list = scan_list.filter(readerLocation=loc)

                the_hour = start
                while the_hour < now:
                    hour_list = filtered_list.filter(added__range=[the_hour, the_hour + delta])
                    if not len(hour_list) == 0:
                        print the_hour
                        print len(hour_list)

                        if len(hour_list) > 1:
                            delete_list = hour_list[1:]
                            print 'delete'
                            print len(delete_list)
                            for item in delete_list:
                                item.delete()

                    the_hour = the_hour + delta
                
