from django.contrib import admin

from models import *

# Register your models here.
admin.site.register(Batch)
admin.site.register(Card)
admin.site.register(Reader)
admin.site.register(Location)
admin.site.register(ReaderLocation)
admin.site.register(Scan)
