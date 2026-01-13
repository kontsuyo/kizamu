from django.contrib import admin

from items.models import BootItem, BootLog

admin.site.register(BootItem)
admin.site.register(BootLog)
