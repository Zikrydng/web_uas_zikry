from django.contrib import admin
from .models import biodata

# Register your models here.
class biodataAdmin(admin.ModelAdmin):
    list_display = ['user','alamat','telpon']
    search_fields = ['user__username']
admin.site.register(biodata, biodataAdmin)
