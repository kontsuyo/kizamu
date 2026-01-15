from django.contrib import admin

from items.models import Item, ItemLog

admin.site.register(Item)
admin.site.register(ItemLog)
