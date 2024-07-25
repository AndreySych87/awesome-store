from django.db import models

from snippets.models import BaseModel
from snippets.models.image import upload_to, ImageMixin

# Create your models here.


class Product(BaseModel):
    """Товар"""

    name = models.CharField('Название', max_length=255, db_index=True)
    description = models.CharField('Описание', max_length=255, null=True, blank=True)
    price = models.FloatField('Базовая цена')
    params = models.ManyToManyField('catalog.ProductParam',
                                    verbose_name='Параметры',
                                    related_name='product_models',
                                    blank=True)

    class Meta:
        ordering = ('ordering',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class ProductImage(ImageMixin, BaseModel):
    """Изображения товара"""

    product = models.ForeignKey('catalog.Product', verbose_name='Товар',
                                related_name='images', on_delete=models.CASCADE)

    image = models.ImageField('Файл', blank=True, upload_to=upload_to)
    description = models.CharField('Описание', max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('ordering',)
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'{self.id}-{self.description}'


class ParamCategory(BaseModel):
    """Категории параметров"""

    title = models.CharField('Заголовок', max_length=255, unique=True)

    slug = models.SlugField(
        'Алиас', max_length=150, db_index=True, unique=True,
        help_text='Разрешены только латинские символы, цифры, символ подчеркивания и дефис (минус)'
    )

    class Meta:
        ordering = ('ordering', 'title')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.title}'


class ProductParam(BaseModel):
    """Параметры товаров"""

    name = models.ForeignKey(
        'catalog.ParamCategory',
        verbose_name='Категория',
        related_name='params',
        on_delete=models.CASCADE
    )

    value = models.CharField('Значение', max_length=255, null=True, blank=True)
    price = models.FloatField('Цена', null=True, blank=True)

    class Meta:
        ordering = ('ordering', 'name__title', 'value')
        verbose_name = 'Параметр товара'
        verbose_name_plural = 'Параметры товара'

    def __str__(self):
        return f'{self.name}: {self.value}'
