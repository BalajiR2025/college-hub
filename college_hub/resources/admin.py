from django.contrib import admin
from .models import Resource, Rating, Report, ResourceRequest

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title','subject','type','uploaded_by','downloads','avg_rating','is_approved']
    list_filter = ['type','is_approved','subject__department']
    search_fields = ['title']
    actions = ['approve_resources']
    def approve_resources(self, request, qs): qs.update(is_approved=True)

admin.register(Rating)(admin.ModelAdmin)
admin.register(Report)(admin.ModelAdmin)
admin.register(ResourceRequest)(admin.ModelAdmin)

