import os

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, get_available_image_extensions


class FileMultipleExtensionValidator(FileExtensionValidator):
    def __call__(self, value):
        for val in value:
            extension = os.path.splitext(val.name)[1][1:].lower()
            if self.allowed_extensions is not None and extension not in self.allowed_extensions:
                raise ValidationError(
                    self.message,
                    code=self.code,
                    params={
                        'extension': extension,
                        'allowed_extensions': ', '.join(self.allowed_extensions)
                    }
                )


validate_image_file_extension_multiple = FileMultipleExtensionValidator(
    allowed_extensions=get_available_image_extensions(),
)
