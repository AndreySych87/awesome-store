from django.contrib.admin.widgets import AdminFileWidget
from django.forms.widgets import FileInput
from django.utils.safestring import mark_safe


class MultipleFileInput(FileInput):
    def __init__(self, attrs=None):
        default_attrs = {'multiple': 'multiple'}
        if attrs:
            default_attrs.update(attrs)
        super(MultipleFileInput, self).__init__(default_attrs)

    def value_from_datadict(self, data, files, name):
        if not files:
            return None
        return files.getlist(name)


class AdminImagePreviewWidget(AdminFileWidget):
    """
    An admin widget that shows a preview of currently selected image.
    """

    def __init__(self, attrs=None, storage=None):
        super(AdminImagePreviewWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, **kwargs):
        content = super(AdminImagePreviewWidget, self).render(name, value, attrs, **kwargs)
        return mark_safe(self._get_preview_tag(value) + content)

    def _get_preview_tag(self, value):
        if value and hasattr(value, "url"):
            return '<img src="{0}" style="max-width: 200px;" /></p>'.format(value.url)

        return ''
