import django_filters
from account.models import Profile

class CustomNumericRangeFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value:
            value_parts = value.split(',')
            if len(value_parts) == 2:
                min_value, max_value = value_parts
                return super().filter(qs, django_filters.fields.Lookup((min_value, max_value), 'range'))
        return super().filter(qs, value)
    
class ProductFilter(django_filters.FilterSet):
    # category__id = django_filters.CharFilter(lookup_expr='iexact')
    # category__name = django_filters.CharFilter(lookup_expr='icontains')
    # name = django_filters.CharFilter(lookup_expr='icontains')
    # description = django_filters.CharFilter(lookup_expr='icontains')
    gender = django_filters.CharFilter(lookup_expr='icontains')
    age = CustomNumericRangeFilter()         
    height = django_filters.NumericRangeFilter()                                                             
    class Meta:
        model = Profile
        fields = ['age', "gender", "height"]
        
#deyis