class BaseMultipleFileUploadAdmin(object):
    def save_model(self, request, obj, form, change):
        result = super(BaseMultipleFileUploadAdmin, self).save_model(request, obj, form, change)
        if form.cleaned_data.get('multiupload', None):
            for image in form.cleaned_data['multiupload']:
                params = {
                    'image': image,
                    self.photo_model_related_name: obj
                }
                self.inline_photo_model.objects.create(**params)
        return result
