from django.contrib import admin

from models import *
from core.actions import export_as_xls

class ScanAdmin(admin.ModelAdmin):
    list_filter = ['readerLocation', 'added']

# Register your models here.
admin.site.register(Batch)
admin.site.register(Card)
admin.site.register(Reader)
admin.site.register(Location)
admin.site.register(ReaderLocation)
admin.site.register(Scan, ScanAdmin)

class MyAdmin(admin.ModelAdmin):
    actions = [export_as_xls]

admin.site.add_action(export_as_xls)
