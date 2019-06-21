from django.shortcuts import render, redirect
from .models import *
from .forms import *
import numbers
from rest_framework import viewsets
from rest_framework.decorators import list_route
from .serializers import *
from django.http import HttpResponse
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from django.db.models import OuterRef, Subquery
from django.contrib.gis.db import models

decimal_filters = {'Trip Distance':'tripDistance','Fare Amount':'fareAmount','Extra':'extra','MTA Tax':'MTATax','Tip amount':'tipAmount',
                    'Tolls amount':'tolls_amount','Improvement Surcharge':'improvementSurcharge','Total Amount':'totalAmount'}
datetime_filters = {'Pickup':'pickup','Dropoff':'dropoff'}
        
# Create your views here.
def read_data(request):
    import pandas as pd
    from django.contrib.gis.geos import Point
    Trip.objects.all().delete()
    def getPoint(lon,lat):
        return Point(lon,lat) if (isinstance(lon,numbers.Real) and lon != 0) else None# return Point(lon,lat)#row['Pickup_longitude'],row['Pickup_latitude'] )#
    
    flag = {'Y': True, 'N': False}
    def csv_row_processing(rows):
        rows['lpep_pickup_datetime'] = pd.to_datetime(rows['lpep_pickup_datetime'])
        rows['Lpep_dropoff_datetime'] = pd.to_datetime(rows['Lpep_dropoff_datetime'])
        rows['Store_and_fwd_flag'] = rows['Store_and_fwd_flag'].map(flag)
        rows['Pickup'] = list(map(getPoint, rows['Pickup_longitude'], rows['Pickup_latitude']))
        rows['Dropoff'] = list(map(getPoint, rows['Dropoff_longitude'], rows['Dropoff_latitude']))
        return rows
    for chunk in pd.read_csv('2016_Green_Taxi_Trip_Data.csv', chunksize=10 ** 3):
        chunk = csv_row_processing(chunk).to_dict('records')
        Trip.objects.bulk_create([Trip(
            vendorID=row['VendorID'],
            pickupTime = row['lpep_pickup_datetime'],
            dropoffTime = row['Lpep_dropoff_datetime'],
            storeAndFwdFlag = row['Store_and_fwd_flag'],
            rateCodeID = row['RateCodeID'],
            pickupPoint = row['Pickup'], #Point(row['Pickup_longitude'],row['Pickup_latitude']) if (isinstance(row['Pickup_longitude'],numbers.Real) and row['Pickup_longitude'] != 0) else None,#,
            dropoffPoint = row['Dropoff'],#Point(row['Dropoff_longitude'],row['Dropoff_latitude']) if (isinstance(row['Dropoff_longitude'],numbers.Real) and row['Dropoff_longitude'] != 0) else None,#,
            passengerCount = row['Passenger_count'],
            tripDistance = row['Trip_distance'],# in miles
            fareAmount = row['Fare_amount'],
            extra = row['Extra'],
            MTATax = row['MTA_tax'],
            tipAmount = row['Tip_amount'],
            tolls_amount = row['Tolls_amount'],
            improvementSurcharge = row['improvement_surcharge'],
            totalAmount = row['Total_amount'],
            paymentType = row['Payment_type'],
            tripType = row['Trip_type '] if isinstance(row['Trip_type '], int) else None,
            PULocationID = row['PULocationID'] if isinstance(row['PULocationID'], int) else None,
            DOLocationID = row['DOLocationID'] if isinstance(row['DOLocationID'], int) else None) for row in chunk]
        )
    return render(request, 'read_data.html', {})

# ViewSets define the view behavior.
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all().prefetch_related('pickupDistrict','dropoffDistrict')#
    serializer_class = TripSerializer
    filter_backends = (OrderingFilter,DjangoFilterBackend,)
    ordering_fields = '__all__'
    filter_class = TripFilter
    
def index(request):
    return render(request, 'index.html')

def trip_list(request):
    return render(request, 'trip_list.html', {'decimal_filters':decimal_filters,'datetime_filters':datetime_filters})
    
def home(request):
    # Tripset.objects.all().get().create_graph()
    return render(request, 'home.html', {})
        
class TripsetViewSet(viewsets.ModelViewSet):
    queryset = Tripset.objects.all()
    serializer_class = TripsetSerializer
    filter_backends = (OrderingFilter,DjangoFilterBackend,)
    ordering_fields = '__all__'
    filter_class = TripsetFilter
    # search_fields = ('name')

    @list_route(methods=['delete'])
    def clear_tripsets(self, request):
        tripsets = Tripset.objects.all()
        tripsets.delete()
        return HttpResponse(status=200)
        # It may be a good idea here to return [].  Not sure.
        
def trip_set_new(request):
    decimal_filter_keywords = []
    datetime_filter_keywords = []
    for f in decimal_filters.values():
        decimal_filter_keywords.append(f+'__gte')
        decimal_filter_keywords.append(f+'__lte')
    for f in datetime_filters.values():
        datetime_filter_keywords.append(f+'__gte')
        datetime_filter_keywords.append(f+'__lte')
    if request.method == "POST":
        form = TripsetForm(request.POST,decimal_filters=decimal_filter_keywords,datetime_filters=datetime_filter_keywords)
        if form.is_valid():
            t = Tripset()
            t.save()
            filters = {}
            for f in decimal_filter_keywords + datetime_filter_keywords:
                if form.data.get(f, False):
                    filters[f] = form.cleaned_data[f]
            t.name=form.cleaned_data['name']
            trips = Trip.objects.filter(**filters).values_list('pk', flat=True)
            if form.data.get('limit', False):
                trips = trips[:form.cleaned_data['limit']]
            t.trips = trips
            t.save()
            form = TripsetForm(decimal_filters=decimal_filter_keywords,datetime_filters=datetime_filter_keywords)
            return render(request, 'trip_set_edit.html', {'form': form,'decimal_filters':decimal_filters,'datetime_filters':datetime_filters})
    else:
        form = TripsetForm(decimal_filters=decimal_filter_keywords,datetime_filters=datetime_filter_keywords)
    return render(request, 'trip_set_edit.html', {'form': form,'decimal_filters':decimal_filters,'datetime_filters':datetime_filters})

def trip_set_list(request):
    sets = Tripset.objects.all()
    return render(request, 'trip_set_list.html', {'sets': sets})
    
def trip_set_detail(request, pk):
    set = get_object_or_404(Tripset, pk=pk)
    return render(request, 'trip_set_detail.html', {'set': set,'decimal_filters':decimal_filters,'datetime_filters':datetime_filters})

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = (OrderingFilter,DjangoFilterBackend,)
    ordering_fields = '__all__'
    #filter_class = TripFilter
    
def project(request,pk):
    from django.contrib.gis.geos import GEOSGeometry
    set = get_object_or_404(Tripset, pk=pk)
    # pickupcity = CityDistrict.objects.filter(shape__contains=OuterRef('pickupPoint'))[:1].values_list('id',flat=True)
    # dropoffcity = CityDistrict.objects.filter(shape__contains=OuterRef('dropoffPoint'))[:1].values_list('id',flat=True)
    # Trip.objects.all().filter(id__lte=10000).exclude(pickupPoint__same_as=GEOSGeometry('POINT EMPTY', srid=4326)).update(pickupDistrict = Subquery(pickupcity),
                         # dropoffDistrict = Subquery(dropoffcity))
                         
    # pickupborough = BoroughDistrict.objects.filter(shape__contains=OuterRef('pickupPoint'))[:1].values_list('id',flat=True)
    # dropoffborough = BoroughDistrict.objects.filter(shape__contains=OuterRef('dropoffPoint'))[:1].values_list('id',flat=True)
    # Trip.objects.all().filter(id__lte=1000,pickupDistrict__isnull=True,pickupPoint__isnull=False).exclude(pickupPoint__same_as=GEOSGeometry('POINT EMPTY', srid=4326)).update(pickupDistrict = Subquery(pickupborough))
    # Trip.objects.all().filter(id__lte=1000,dropoffDistrict__isnull=True,dropoffPoint__isnull=False).exclude(dropoffPoint__same_as=GEOSGeometry('POINT EMPTY', srid=4326)).update(dropoffDistrict = Subquery(dropoffborough))
    # set.get_trips().exclude(pickupPoint__same_as=GEOSGeometry('POINT EMPTY', srid=4326)).update(pickupDistrict = Subquery(pickupcity),
                         # dropoffDistrict = Subquery(dropoffcity))
    
    # for d in CityDistrict.objects.all():
        # set.get_trips().filter(pickupPoint__coveredby=d.shape).update(pickupDistrict = d.id)
        # set.get_trips().filter(dropoffPoint__coveredby=d.shape).update(dropoffDistrict = d.id)
    return render(request, 'trip_set_detail.html', {'set': set})

def create_graph(request,pk):
    set = get_object_or_404(Tripset, pk=pk)
    set.create_graph()
    return render(request, 'trip_set_detail.html', {'set': set})
    
class EdgeViewSet(viewsets.ModelViewSet):
    queryset = Edge.objects.all().prefetch_related('tail','head')
    serializer_class = EdgeSerializer
    filter_backends = (OrderingFilter,DjangoFilterBackend,)
    filter_class = EdgeFilter
    ordering_fields = '__all__'
    
class MatrixEdgeViewSet(viewsets.ModelViewSet):
    queryset = Edge.objects.all().prefetch_related('tail','head')
    serializer_class = MatrixEdgeSerializer
    filter_backends = (OrderingFilter,DjangoFilterBackend,)
    filter_class = EdgeFilter
    ordering_fields = '__all__'