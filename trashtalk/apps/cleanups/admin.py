from django.contrib import admin

from .models import Cleanup, Location, RequiredTools, Tool, ToolCategory

class ToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter  = ['category']


# Register your models here.
admin.site.register(Cleanup)
admin.site.register(Location)
admin.site.register(RequiredTools)
admin.site.register(Tool, ToolAdmin)
admin.site.register(ToolCategory)