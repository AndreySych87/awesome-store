from django.contrib import admin
from django.contrib.admin import FieldListFilter
from django.utils.translation import ugettext_lazy as _


class IsNullFieldListFilter(FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__isnull' % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)

        super(IsNullFieldListFilter, self).__init__(
            field, request, params, model, model_admin, field_path
        )

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def choices(self, cl):
        for lookup, title in (
                (None, _('All')),
                ('False', _('Yes')),
                ('True', _('No'))
        ):
            yield {
                'selected': self.lookup_val == lookup,
                'query_string': cl.get_query_string({
                    self.lookup_kwarg: lookup,
                }),
                'display': title,
            }


class AdminListFilter(admin.SimpleListFilter):
    template = 'filters/drop_down_filter.html'
    title = None
    parameter_name = None
    rel_model = None

    def lookups(self, request, model_admin):
        return list(
            map(
                lambda x: (x.id, x.title),
                self.rel_model.objects.all().order_by('title')
            )
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value:
            return queryset.filter(**{self.parameter_name: value})


def AdminListFilterFactory(title, param_name, rel_model):
    class NewFilter(AdminListFilter):
        def __init__(self, request, params, model, model_admin):
            self.rel_model = rel_model
            self.title = title
            self.parameter_name = param_name
            super().__init__(request, params, model, model_admin)

    return NewFilter
