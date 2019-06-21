from .models import *
from rest_framework import serializers, pagination
from django.core.paginator import Paginator
import django_filters

# Serializers define the API representation.
class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District
        fields = ('name',)

class TripSerializer(serializers.HyperlinkedModelSerializer):
    #pickupDistrict = DistrictSerializer(read_only=True)DistrictSerializer(read_only=True)
    pickupDistrict = serializers.StringRelatedField(many=False)
    dropoffDistrict = serializers.StringRelatedField(many=False)
    class Meta:
        model = Trip
        fields = ('pickupTime','pickupPoint','dropoffPoint','totalAmount','tripDistance','pickupDistrict','dropoffDistrict')#

# class PaginatedTripSerializer(pagination.PaginationSerializer):
    # class Meta:
        # object_serializer_class = TripSerializer
        
WEEKDAY_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
)

class TripFilter(django_filters.FilterSet):
    pickupTime__gte = django_filters.IsoDateTimeFilter(name="pickupTime", lookup_expr='gte')
    pickupTime__lte = django_filters.IsoDateTimeFilter(name="pickupTime", lookup_expr='lte')
    pickupWeekday = django_filters.TypedMultipleChoiceFilter(choices=WEEKDAY_CHOICES,name="pickupTime__week_day")
    #pickupWeekday = django_filters.NumberFilter(method='weekday_filter')
    dropoffTime__gte = django_filters.IsoDateTimeFilter(name="dropoffTime", lookup_expr='gte')
    dropoffTime__lte = django_filters.IsoDateTimeFilter(name="dropoffTime", lookup_expr='lte')
    # dropoffWeekday = django_filters.MultipleChoiceFilter(choices=WEEKDAY_CHOICES,name="dropoffTime", lookup_expr='week_day')
    set = django_filters.NumberFilter(method='set_filter')
    class Meta:
        model = Trip
        fields = {
            'tripDistance': ['lte', 'gte'],
            'totalAmount': ['lte', 'gte'],
        }
    def set_filter(self, queryset, name, value):
        if value == 29:
            return queryset#.filter(pickupDistrict__isnull=True,pickupPoint__isnull=False)
        return queryset.filter(set=value)
    
    # def weekday_filter(self, queryset, name, value):
        # return queryset.filter(pickupTime__week_day=value)
        
class TripsetSerializer(serializers.HyperlinkedModelSerializer):
    trips = serializers.SerializerMethodField('paginated_trips')#TripSerializer(many=True, read_only=True)

    class Meta:
        model = Tripset
        fields = ('id','name', 'trips')#
    
    def paginated_trips(self, obj):
        trips = Trip.objects.filter(set=obj)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(trips, self.context['request'])
        serializer = TripSerializer(page, many=True, context={'request': self.context['request']})
        return serializer.data
        
class TripsetFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    min_id = django_filters.NumberFilter(name="id", lookup_expr='gte')
    max_id = django_filters.NumberFilter(name="id", lookup_expr='lte')

    class Meta:
        model = Tripset
        fields = ['name','id']
        
class EdgeSerializer(serializers.HyperlinkedModelSerializer):
    tail = serializers.StringRelatedField(many=False)
    head = serializers.StringRelatedField(many=False)
    class Meta:
        model = Edge
        fields = ('tail','head','weight')#

class MatrixEdgeSerializer(serializers.HyperlinkedModelSerializer):
    source = serializers.StringRelatedField(many=False,source='tail')
    target = serializers.StringRelatedField(many=False,source='head')
    value = serializers.FloatField(source='weight')
    class Meta:
        model = Edge
        fields = ('source','target','value')#
        
class EdgeFilter(django_filters.FilterSet):
    # # tripset__id = django_filters.NumberFilter(lookup_expr='exact')
    # tripset__name = django_filters.CharFilter(lookup_expr='icontains')
    weight__gte = django_filters.NumberFilter(name='weight', lookup_expr='gte')
    weight__lte = django_filters.NumberFilter(name='weight', lookup_expr='lte')
    class Meta:
        model = Edge
        fields = '__all__'#[]