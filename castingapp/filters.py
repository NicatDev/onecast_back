import django_filters
from account.models import Profile

class ProductFilter(django_filters.FilterSet):
    # category__id = django_filters.CharFilter(lookup_expr='iexact')
    # category__name = django_filters.CharFilter(lookup_expr='icontains')
    # name = django_filters.CharFilter(lookup_expr='icontains')
    # description = django_filters.CharFilter(lookup_expr='icontains')
    gender = django_filters.CharFilter(lookup_expr='icontains')
    age = django_filters.NumericRangeFilter()         
    height = django_filters.NumericRangeFilter()                                                             
    class Meta:
        model = Profile
        fields = ['age', "gender", "height"]
        
#deyis