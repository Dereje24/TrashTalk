from django.contrib import admin

from .models import Cleanup, Location, CleanupTools, Tool

# Register your models here.
admin.site.register(Cleanup)
admin.site.register(Location)
admin.site.register(CleanupTools)
admin.site.register(Tool)
