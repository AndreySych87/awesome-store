from django.db import models
from django.db.models import ForeignKey
from django.db.models import Manager
from django.db.models import QuerySet


from snippets.models.enumerates import StatusEnum

CREATED_VERBOSE = 'Создано'
UPDATED_VERBOSE = 'Обновлено'
LASTMOD_FIELDS = ('created', 'updated')
UTIL_FIELDS = ('id', 'ordering', 'status') + LASTMOD_FIELDS


class BaseQuerySet(QuerySet):
    def published(self):
        return self.filter(status__exact=StatusEnum.PUBLIC)

    def hidden(self):
        return self.filter(status__exact=StatusEnum.HIDDEN)

    def draft(self):
        return self.filter(status__exact=StatusEnum.DRAFT)


BaseManager = Manager.from_queryset(BaseQuerySet)


class BasicModel(models.Model):
    translation_fields = tuple()
    objects = Manager()

    def collect_fields(self):
        fields = []
        has_status = False
        has_ordering = False
        has_last_mod = False

        for field in self._meta.fields:
            if field.attname == 'status':
                has_status = True

            if field.attname == 'ordering':
                has_ordering = True

            if field.attname in LASTMOD_FIELDS:
                has_last_mod = True

            if field.attname in UTIL_FIELDS:
                continue

            if isinstance(field, ForeignKey):
                fields.append(field.attname.replace('_id', ''))
            else:
                fields.append(field.attname)

        # служебные поля в самый конец
        if has_status:
            fields.append('status')

        if has_ordering:
            fields.append('ordering')

        if has_last_mod:
            fields.extend(LASTMOD_FIELDS)

        return fields

    def __repr__(self):
        return self.__str__()

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    """Base model for all models with created field"""
    created = models.DateTimeField(CREATED_VERBOSE, auto_now_add=True, db_index=True)

    class Meta:
        abstract = True


class LastModModel(CreatedModel):
    """Base model for all models with created / updated fields"""
    updated = models.DateTimeField(UPDATED_VERBOSE, auto_now=True)

    class Meta:
        abstract = True


class LastModMixin(models.Model):
    """Base model for all models with created / updated fields"""
    created = models.DateTimeField(CREATED_VERBOSE, auto_now_add=True, db_index=True)
    updated = models.DateTimeField(UPDATED_VERBOSE, auto_now=True)

    class Meta:
        abstract = True


class StatusOrderingModel(models.Model):
    """Base model for all objects"""
    ordering = models.IntegerField('Порядок', default=0, db_index=True)
    status = models.SmallIntegerField(
        'Статус',
        default=StatusEnum.PUBLIC,
        choices=StatusEnum.get_choices()
    )

    class Meta:
        abstract = True


class BaseModel(StatusOrderingModel, BasicModel, LastModModel):
    """Base model class for all models having last-mod fields and status with ordering"""
    objects = BaseManager()

    class Meta:
        abstract = True
