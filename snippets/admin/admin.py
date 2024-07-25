from django.contrib.admin import ModelAdmin
from django.db.models import ImageField, FileField
# from django_admin_inline_paginator.admin import TabularInlinePaginated, PaginationFormSetBase
# from solo.admin import SingletonModelAdmin

from snippets.admin import actions
from snippets.forms.widgets import AdminImagePreviewWidget
from snippets.models.image import SVGAndImageField


class SuperUserDeletableAdminMixin(object):
    @staticmethod
    def has_delete_permission(request, obj=None):
        return request.user.is_superuser


class BaseModelAdmin(ModelAdmin):
    """Базовый класс для админ.части модели BaseModel"""
    actions = ModelAdmin.actions + [actions.publish, actions.hide, actions.to_drafts]
    list_display = ('id', 'status', 'ordering', 'created')
    list_editable = ('status', 'ordering')
    list_filter = ('status',)
    ordering = ('ordering',)
    readonly_fields = ('created', 'updated')
    search_fields = ['=id']
    save_as = True

    formfield_overrides = {
        ImageField: {'widget': AdminImagePreviewWidget},
        SVGAndImageField: {'widget': AdminImagePreviewWidget},
    }

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(BaseModelAdmin, self).get_fieldsets(request, obj=obj)

        for field in ('created', 'updated'):
            if field not in fieldsets[0][1]['fields']:
                fieldsets[0][1]['fields'].append(field)

        return fieldsets


class ImageAdminMixin:
    formfield_overrides = {
        ImageField: {'widget': AdminImagePreviewWidget},
        FileField: {'widget': AdminImagePreviewWidget}
    }
