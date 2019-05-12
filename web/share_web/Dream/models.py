from __future__ import unicode_literals

from django.db import models

import magic
from django import forms

from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat


@deconstructible
class FileValidator(object):
    error_messages = {
     'max_size': ("Ensure this file size is not greater than %(max_size)s."
                  " Your file size is %(size)s."),
     'min_size': ("Ensure this file size is not less than %(min_size)s. "
                  "Your file size is %(size)s."),
     'content_type': "Files of type %(content_type)s are not supported.",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise forms.ValidationError(self.error_messages['max_size'],
                                   'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.mix_size),
                'size': filesizeformat(data.size)
            }
            raise forms.ValidationError(self.error_messages['min_size'],
                                   'min_size', params)

        if self.content_types:
            data.seek(0)
            content_type = magic.from_buffer(data.read(), mime=True)

            if content_type in self.content_types:
                params = { 'content_type': content_type }
                raise forms.ValidationError(self.error_messages['content_type'],
                                   'content_type', params)

    def __eq__(self, other):
        return (
            isinstance(other, FileValidator) and
            self.max_size == other.max_size and
            self.min_size == other.min_size and
            self.content_types == other.content_types
        )


class Document(models.Model):
    #validate_file = FileValidator(content_types=('application/x-dosexec'))
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='')
    size = models.CharField(max_length=255, blank=True)
    md5 = models.CharField(max_length=255, blank=True)
    types = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
