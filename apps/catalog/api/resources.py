from rest_framework.generics import RetrieveAPIView
from django.db.models import Count

from catalog import models
from catalog.api import serializers, filters
from rest_framework.viewsets import ReadOnlyModelViewSet


class ParamViewSet(ReadOnlyModelViewSet):
    """Параметры"""
    queryset = models.ParamCategory.objects.published()
    serializer_class = serializers.ParamCategorySerializer
    pagination_class = None

    def get_queryset(self):
        qs = self.queryset
        qs = qs.annotate(
            product_count=Count("params__product_models")).filter(product_count__gt=0)
        return qs


class ProductModelViewSet(ReadOnlyModelViewSet):
    """Товары"""
    queryset = models.Product.objects.published()
    filterset_class = filters.ProductModelFilter
    pagination_class = None

    def get_serializer_class(self):
        serializer_map = {
            'list': serializers.ProductModelListSerializer,
            'retrieve': serializers.ProductDetailSerializer,
        }
        return serializer_map[self.action]
