from django.contrib.gis.db import models
from django.core.cache import cache
# Create your models here.

class Trip(models.Model):
    # class Meta:
    #    db_table = 'taxi_trip_timescale'
    vendorID = models.SmallIntegerField(null=True,blank=True)
    pickupTime = models.DateTimeField(null=True,blank=True)
    dropoffTime = models.DateTimeField(null=True,blank=True)
    storeAndFwdFlag = models.BooleanField() #Y(TRUE)= store and forward trip  N(FALSE)= not a store and forward trip
    rateCodeID = models.SmallIntegerField(null=True,blank=True)
    pickupPoint = models.PointField(null=True,blank=True)
    dropoffPoint = models.PointField(null=True,blank=True)
    passengerCount = models.SmallIntegerField(null=True,blank=True)
    tripDistance = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)# in miles
    fareAmount = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    extra = models.DecimalField(max_digits=4, decimal_places=2,null=True,blank=True)
    MTATax = models.DecimalField(max_digits=3, decimal_places=2,null=True,blank=True)
    tipAmount = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    tolls_amount = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    # Ehail_fee : All NULL
    improvementSurcharge = models.DecimalField(max_digits=3, decimal_places=2,null=True,blank=True)
    totalAmount = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    paymentType = models.SmallIntegerField(null=True,blank=True)
    tripType = models.SmallIntegerField(null=True,blank=True)
    PULocationID = models.SmallIntegerField(null=True,blank=True)
    DOLocationID = models.SmallIntegerField(null=True,blank=True)
    pickupDistrict = models.ForeignKey('District', related_name='trips_by_pickup', null=True)
    dropoffDistrict = models.ForeignKey('District', related_name='trips_by_dropoff',null=True)
    objects = models.GeoManager()
    
    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return str(self.pickupTime)
        
    # @property
    # def pickup(self):
        # if self.pickupPoint is None:
            # return ''
        # precision = "{:.5f}" 
        # return '('+precision.format(self.pickupPoint.x)+','+precision.format(self.pickupPoint.y)+')'

    # @property
    # def dropoff(self):
        # if self.dropoffPoint is None:
            # return ''
        # precision = "{:.5f}" 
        # return '('+precision.format(self.dropoffPoint.x)+','+precision.format(self.dropoffPoint.y)+')'

class Tripset(models.Model):
    name = models.CharField(max_length=200)
    trips = models.ManyToManyField(Trip, blank=True,related_name='set')#, through='TripInSet'
    def __str__(self):
        return self.name
    
    def create_graph(self):
        from django.db.models import Count
        edges = self.get_trips().filter(pickupDistrict__isnull=False, dropoffDistrict__isnull=False).values('pickupDistrict','dropoffDistrict').order_by().annotate(weight=Count('pk'))
        Edge.objects.all().filter(tripset = self).delete()
        Edge.objects.bulk_create([Edge(
            tail_id = e['pickupDistrict'],
            head_id = e['dropoffDistrict'],
            weight = e['weight'],
            tripset = self) for e in edges])
        return 0
        
    def n_trips(self):
        key = "set_"+str(self.pk)+"_count_trips"
        count = cache.get(key)
        if count is None:
            count = self.get_trips().count()
            cache.set(key,count,72*3600) #timeout 3 days
        return count#self.trips.count()
    
    def get_trips(self):
        if self.pk is 29:
            return Trip.objects.all()
        return self.trips.all()
# class TripInSet(models.Model):
    # trip = models.ForeignKey(Trip, related_name='set')
    # tripset = models.ForeignKey(Tripset, related_name='info')
    # pickupDistrict = models.ForeignKey(District,null=True)
    # dropoffDistrict = models.ForeignKey(District,null=True)

class Edge(models.Model):
    tail = models.ForeignKey('District',related_name='edges_as_tail')
    head = models.ForeignKey('District',related_name='edges_as_head')
    weight = models.FloatField(null=True)
    tripset = models.ForeignKey(Tripset, null=True, related_name='graph', on_delete=models.CASCADE)
    
class District(models.Model):
    name = models.CharField(max_length=256)
    center = models.PointField(null=True)
    shape = models.MultiPolygonField()
    objects = models.GeoManager()
    #area_square_local_units = object.polygon.transform(srid, clone=False).area
    def __str__(self):
        return self.name

class BoroughDistrict(District):
    fip = models.CharField(max_length=5)

class CityDistrict(District):
    borough = models.ForeignKey('BoroughDistrict')
    ntacode = models.CharField(max_length=5)
    area = models.FloatField()