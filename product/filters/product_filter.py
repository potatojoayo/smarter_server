import django_filters

from product.models import Product
from django.contrib.postgres.search import SearchVector, SearchQuery

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')
    product_master__category__name = django_filters.CharFilter(lookup_expr='exact')
    product_master__sub_category__name = django_filters.CharFilter(lookup_expr='exact')
    product_master__brand__name = django_filters.CharFilter(lookup_expr='exact')


    class Meta:
        model = Product
        fields = ['name', 'product_master__category__name', 'product_master__sub_category__name', 'product_master__brand__name']

    def filter_name(self, queryset, name, value):
        search_terms = value.split(' ')
        print('filter_name')
        for term in search_terms:
            queryset = queryset.filter(name__icontains=term)
        return queryset