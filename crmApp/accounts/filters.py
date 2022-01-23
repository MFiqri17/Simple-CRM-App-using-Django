from django.db.models import fields
from django.db.models.lookups import IContains
import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class OrderFilter(django_filters. FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')
    search = CharFilter(field_name='product', lookup_expr=IContains)
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['custoemer', 'date_created']