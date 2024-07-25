import sys
import xml.etree.cElementTree as et
from io import BytesIO

import six
from PIL import Image
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    get_available_image_extensions,
    EMPTY_VALUES
)
from django.forms import FileField, ImageField
from django.forms import ImageField as DjangoImageField

from snippets.forms import validators
from snippets.forms.widgets import MultipleFileInput


class MultipleFileField(FileField):
    widget = MultipleFileInput
    empty_values = list(EMPTY_VALUES)

    def to_python(self, data):
        if data in self.empty_values:
            return None
        for data_item in data:
            self.data_item_to_python(data_item)
        return data

    def data_item_to_python(self, data):
        if data is None:
            return None

        try:
            file_name = data.name
            file_size = data.size
        except AttributeError:
            raise ValidationError(self.error_messages['invalid'], code='invalid')

        if self.max_length is not None and len(file_name) > self.max_length:
            params = {
                'max': self.max_length,
                'length': len(file_name),
            }
            raise ValidationError(
                self.error_messages['max_length'], code='max_length', params=params
            )

        if not file_name:
            raise ValidationError(self.error_messages['invalid'], code='invalid')

        if not self.allow_empty_file and not file_size:
            raise ValidationError(self.error_messages['empty'], code='empty')

        return data


class MultipleImageField(MultipleFileField, ImageField):
    default_validators = [validators.validate_image_file_extension_multiple]

    def data_item_to_python(self, data):
        """
        Checks that uploaded data contains a valid image
        (GIF, JPG, PNG or whatever the PIL supports)
        See ImageField at https://github.com/django/django/blob/stable/1.5.x/django/forms/
        fields.py for details
        """
        data = super(MultipleImageField, self).data_item_to_python(data)

        # PIL is required to verify file

        if hasattr(data, 'temporary_file_path'):
            data_file = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                data_file = six.BytesIO(data.read())
            else:
                data_file = six.BytesIO(data['content'])

        try:
            # Image.verify() must be called immediately after the constructor
            Image.open(data_file).verify()
        except Exception:
            raise ValidationError(self.error_messages['invalid_image'])

        if hasattr(data, 'seek') and callable(data.seek):
            data.seek(0)

        return data


def validate_image_and_svg_file_extension(value):
    allowed_extensions = get_available_image_extensions() + ["svg"]
    return FileExtensionValidator(allowed_extensions=allowed_extensions)(value)


class SVGAndImageFormField(DjangoImageField):
    """
    Example usage
    class Image(models.Model):
        image = models.ImageField()

    class ImageSerializer(serializers.ModelSerializer):
        image = serializers.ImageField(_DjangoImageField=SVGAndImageFormField)

        class Meta:
            model = Image
            fields = "__all__"
    """
    default_validators = [validate_image_and_svg_file_extension]

    def to_python(self, data):
        """
        Checks that the file-upload field data contains a valid image (GIF, JPG,
        PNG, possibly others -- whatever the Python Imaging Library supports).
        """
        test_file = super(DjangoImageField, self).to_python(data)
        if test_file is None:
            return None

        # We need to get a file object for Pillow. We might have a path or we might
        # have to read the data into memory.
        if hasattr(data, "temporary_file_path"):
            ifile = data.temporary_file_path()
        else:
            if hasattr(data, "read"):
                ifile = BytesIO(data.read())
            else:
                ifile = BytesIO(data["content"])

        try:
            # load() could spot a truncated JPEG, but it loads the entire
            # image in memory, which is a DoS vector. See #3848 and #18520.
            image = Image.open(ifile)
            # verify() must be called immediately after the constructor.
            image.verify()

            # Annotating so subclasses can reuse it for their own validation
            test_file.image = image
            test_file.content_type = Image.MIME[image.format]
        except Exception:
            # add a workaround to handle svg images
            if not self.is_svg(ifile):
                raise ValidationError(
                    self.error_messages["invalid_image"], code="invalid_image",
                ).with_traceback(sys.exc_info()[2])
        if hasattr(test_file, "seek") and callable(test_file.seek):
            test_file.seek(0)
        return test_file

    def is_svg(self, f):
        """
        Check if provided file is svg
        """
        f.seek(0)
        tag = None
        try:
            for event, el in et.iterparse(f, ("start",)):
                tag = el.tag
                break
        except et.ParseError:
            pass
        return tag == "{http://www.w3.org/2000/svg}svg"
