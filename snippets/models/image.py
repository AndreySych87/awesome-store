import uuid
from typing import Optional

from django.conf import settings
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils.html import format_html
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import EasyThumbnailsError

from snippets.forms.fields import SVGAndImageFormField


def upload_to(instance, filename):
    model_name = instance.__class__.__name__.lower()
    prefix = uuid.uuid4().hex[:2]
    app_name = instance._meta.app_label.lower()
    file_path = f'{app_name}/{model_name}/{prefix}/{filename}'
    return file_path


class ImageMixin(models.Model):
    image_field = 'image'
    image_size = (70, 40)

    def is_svg(self, image):
        if image and isinstance(image, ImageFieldFile):
            return image.path.endswith('.svg')
        return False

    def image_thumb(self, field_name: Optional[str] = None, size=None):
        if size is None:
            size = self.image_size

        img_attr = field_name if field_name else self.image_field
        image = getattr(self, img_attr)
        if (image and not isinstance(image, ImageFieldFile)) or self.is_svg(image):
            return format_html('<img src="%s" alt="" style="max-width:%spx;max-height:%spx;">' % (
                image.url, size[0], size[1]
            ))
        else:
            try:
                return format_html(
                    '<img src="%s" alt="" />' % get_thumbnailer(
                        getattr(self, img_attr)
                    ).get_thumbnail({
                        'size': size,
                        'detail': True,
                    }).url if image else '<img src="%simages/blank.gif" alt="" '
                                         'style="max-width:%spx;max-height:%spx;" />' % (
                                             settings.STATIC_URL, size[0], size[1]
                                         )
                )
            except (OSError, EasyThumbnailsError):
                return ''

    image_thumb.short_description = 'Изображение'

    class Meta:
        abstract = True


class SVGAndImageField(models.ImageField):
    def formfield(self, **kwargs):
        defaults = {'form_class': SVGAndImageFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
