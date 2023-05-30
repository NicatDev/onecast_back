import django_filters
from account.models import Profile
from castingapp.models import News

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
    is_child = django_filters.BooleanFilter()
    is_actor = django_filters.BooleanFilter()
    is_model = django_filters.BooleanFilter()
    gender = django_filters.CharFilter(lookup_expr='icontains')
    age = django_filters.RangeFilter()        
    height = django_filters.RangeFilter()                                                         
    class Meta:
        model = Profile
        fields = ['age', "gender", "height",'is_actor','is_model','is_child']
         
#deyis

class MagazineFilter(django_filters.FilterSet):
    # category__id = django_filters.CharFilter(lookup_expr='iexact')
    # category__name = django_filters.CharFilter(lookup_expr='icontains')
    # name = django_filters.CharFilter(lookup_expr='icontains')
    # description = django_filters.CharFilter(lookup_expr='icontains')
    title = django_filters.CharFilter(lookup_expr='icontains')
                                                       
    class Meta:
        model = News
        fields = ['title']