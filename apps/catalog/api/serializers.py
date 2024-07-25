from rest_framework import serializers
from django.db.models import Count

from snippets.models.enumerates import StatusEnum
from catalog import models


class ProductImageSerializer(serializers.ModelSerializer):
    """Изображения товара"""
    class Meta:
        model = models.ProductImage
        fields = ('id', 'image', 'description')


class ProductParamSerializer(serializers.ModelSerializer):
    """Параметры товара"""
    class Meta:
        model = models.ProductParam
        fields = ('id', 'name', 'value', 'price')


class ParamCountProductSerializer(serializers.ModelSerializer):
    """Параметры товара"""
    count_prod = serializers.SerializerMethodField()

    class Meta:
        model = models.ProductParam
        fields = ('id', 'name', 'value', 'price', 'count_prod')

    def get_count_prod(self, obj):
        items = models.Product.objects.filter(
            params=obj.id,
            status=StatusEnum.PUBLIC
            ).count()
        return items


class ParamCategorySerializer(serializers.ModelSerializer):
    """Категории параметров"""

    params = serializers.SerializerMethodField()

    class Meta:
        model = models.ParamCategory
        fields = ('id', 'title', 'slug', 'params')

    def get_params(self, obj):
        items = models.ProductParam.objects.annotate(
            product_count=Count("product_models")
            ).filter(
            name=obj.id,
            product_count__gt=0,
            status=StatusEnum.PUBLIC
            )
        return ParamCountProductSerializer(items, many=True).data


class ProductModelListSerializer(serializers.ModelSerializer):
    """Список товаров"""

    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()

    class Meta:
        model = models.Product
        fields = ('id', 'name', 'description', 'price')


class ProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    params = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = (
            'id', 'name', 'description', 'price',
            'images', 'params'
        )

    def get_images(self, obj):
        items = models.ProductImage.objects.filter(
            product=obj.id,
            status=StatusEnum.PUBLIC
            )
        return ProductImageSerializer(items, many=True).data

    def get_params(self, obj):
        items = models.ProductParam.objects.filter(
            status=StatusEnum.PUBLIC,
            product_models=obj.id
            )
        return ProductParamSerializer(items, many=True).data
