from snippets.models.enumerates import StatusEnum


def deactivate_action(modeladmin, request, queryset):
    queryset.update(is_active=False)


deactivate_action.short_description = 'Деактивировать'


def activate_action(modeladmin, request, queryset):
    queryset.update(is_active=True)


activate_action.short_description = 'Активировать'


def publish(modeladmin, request, queryset):
    queryset.update(status=StatusEnum.PUBLIC)


publish.short_description = 'Опубликовать'


def hide(modeladmin, request, queryset):
    queryset.update(status=StatusEnum.HIDDEN)


hide.short_description = 'Скрыть'


def to_drafts(modeladmin, request, queryset):
    queryset.update(status=StatusEnum.DRAFT)


to_drafts.short_description = 'В черновики'
