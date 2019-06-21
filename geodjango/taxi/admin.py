from django.contrib.gis import admin
#from django.contrib import admin
from .models import Trip, BoroughDistrict, CityDistrict, Tripset, Edge
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget
# Register your models here.

class TripAdmin(admin.ModelAdmin):
    #pass
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    list_display = ('pickupTime','pickupPoint','dropoffPoint','totalAmount')
    modifiable = False
#admin.site.register(Trip, admin.GeoModelAdmin)
admin.site.register(Trip,TripAdmin)

class BoroughAdmin(admin.ModelAdmin):
    list_display = ('name','fip')
admin.site.register(BoroughDistrict,BoroughAdmin)

class CityDistrictAdmin(admin.ModelAdmin):
    list_display = ('name','ntacode')
admin.site.register(CityDistrict,CityDistrictAdmin)

admin.site.register(Tripset)

class EdgeAdmin(admin.ModelAdmin):
    list_display = ('tail','head','weight','tripset')
admin.site.register(Edge,EdgeAdmin)