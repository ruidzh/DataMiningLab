import xadmin
from .models import Trip
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget
# Register your models here.

# class TripAdmin(admin.ModelAdmin):
    # #pass
    # formfield_overrides = {
        # models.PointField: {"widget": GooglePointFieldWidget}
    # }
    # list_display = ('pickupTime','pickupPoint','dropoffPoint','totalAmount')
class TripAdmin(object):
    list_display = ('pickupTime','pickupPoint','dropoffPoint','totalAmount')
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    # data_charts = {
        # "user_count": {'title': u"totalAmount Report", "x-field": "date", "y-field": ("user_count", "view_count"), "order": ('date',)},
        # "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)}
    # }
    modifiable = False
    
xadmin.site.register(Trip,TripAdmin)