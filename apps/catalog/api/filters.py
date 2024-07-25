import decimal

from catalog import models
from django.db.models import F
from django_filters import rest_framework as filters
from snippets.models.enumerates import StatusEnum


class ProductModelFilter(filters.FilterSet):
    """Фильтры для товаров"""
    param_name = filters.CharFilter(method='get_for_param_name')
    param_value = filters.CharFilter(method='get_for_param_value')

    class Meta:
        model = models.Product
        fields = ('param_name', 'param_value')

    @staticmethod
    def get_for_param_name(queryset, name, value):
        """Фильтр по названию параметра"""
        if value:
            queryset = queryset \
                .filter(params__name__slug=value,
                        params__status__exact=StatusEnum.PUBLIC) \
                .published() \
                .distinct() \
                .order_by('ordering')

        return queryset

    @staticmethod
    def get_for_param_value(queryset, name, value):
        """Фильтр по значению параметра"""
        if value:
            queryset = queryset \
                .filter(params__value=value,
                        params__status__exact=StatusEnum.PUBLIC) \
                .published() \
                .distinct() \
                .order_by('ordering')

        return queryset
