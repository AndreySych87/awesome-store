from django.contrib import admin
from catalog import models
from tabbed_admin import TabbedModelAdmin

from snippets.admin import BaseModelAdmin
from snippets.admin.admin import ImageAdminMixin

# Register your models here.


@admin.register(models.ParamCategory)
class ParamCategoryAdmin(BaseModelAdmin):
    """Параметры товаров"""

    fields = models.ParamCategory().collect_fields()
    list_display = ('id', 'title', 'slug', 'status',
                    'ordering', 'created')
    list_display_links = ('id', 'title')
    list_filter = BaseModelAdmin.list_filter
    ordering = ('ordering', 'title')
    search_fields = ['=id', 'title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.ProductParam)
class ProductParamAdmin(BaseModelAdmin):
    """Параметры товаров"""

    fields = models.ProductParam().collect_fields()
    list_display = ('id', 'name', 'value', 'price', 'status',
                    'ordering', 'created')
    list_display_links = ('id', 'name')
    list_filter = BaseModelAdmin.list_filter
    ordering = ('ordering', 'name', 'value')
    search_fields = ['=id', 'name', 'value']


class ProductImageInline(ImageAdminMixin, admin.TabularInline):
    """Изображения товара"""

    extra = 0
    fields = models.ProductImage().collect_fields()
    model = models.ProductImage
    ordering = ('ordering', '-created')
    readonly_fields = ('created', 'updated')


@admin.register(models.Product)
class ProductAdmin(TabbedModelAdmin):
    """Товар"""
    model = models.Product

    list_display = ('id', 'name', 'description', 'price',
                    'status', 'created', 'updated', 'ordering')
    list_display_links = ('id', 'name')
    search_fields = ['=id', 'name', 'description']
    readonly_fields = ('created', 'updated')
    list_editable = ('status', 'ordering')
    list_filter = ('status',)
    ordering = ('ordering',)

    filter_horizontal = (
        'params',
    )
    tab_overview = (
        (None, {
            'fields': ('name', 'description', 'price',
                       'status', 'created', 'ordering', 'params')
        }),
    )
    tab_img = (ProductImageInline,)

    tabs = [
        ('Основное', tab_overview),
        ('Изображения товара', tab_img),
    ]
