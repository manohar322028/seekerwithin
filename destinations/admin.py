from django.contrib import admin

# Register your models here.

from .models import Destination, DestinationImage

admin.site.register(Destination)
admin.site.register(DestinationImage)