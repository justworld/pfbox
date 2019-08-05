# coding: utf-8
from django.db import models
from django.core import exceptions
from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _


class MinChoicesValidator(validators.MinLengthValidator):
    message = _(u'需要至少选择%(limit_value)d个选项')
    code = 'min_choices'


class MaxChoicesValidator(validators.MaxLengthValidator):
    message = _(u'最多只能选择%(limit_value)d个选项')
    code = 'max_choices'


class MultiSelectFormField(forms.MultipleChoiceField):

    def __init__(self, *args, **kwargs):
        self.min_choices = kwargs.pop('min_choices', None)
        self.max_choices = kwargs.pop('max_choices', None)
        self.max_length = kwargs.pop('max_length', None)
        super(MultiSelectFormField, self).__init__(*args, **kwargs)
        if self.max_choices is not None:
            self.validators.append(MaxChoicesValidator(self.max_choices))
        if self.min_choices is not None:
            self.validators.append(MinChoicesValidator(self.min_choices))


class MultiSelectField(models.CharField):
    """
    from django-multiselectfield
    多选字段
    """

    def __init__(self, *args, **kwargs):
        self.min_choices = kwargs.pop('min_choices', None)
        self.max_choices = kwargs.pop('max_choices', None)
        super(MultiSelectField, self).__init__(*args, **kwargs)

    def _get_flatchoices(self):
        l = super(MultiSelectField, self)._get_flatchoices()

        class MSFFlatchoices(list):
            def __bool__(self):
                return False

            __nonzero__ = __bool__

        return MSFFlatchoices(l)

    flatchoices = property(_get_flatchoices)

    def get_db_prep_save(self, value, connection):
        value = super(MultiSelectField, self).get_db_prep_save(value, connection)
        if isinstance(value, set):
            value = list(value)
        if value:
            return ','.join(str(x) for x in value)
        return ''

    def from_db_value(self, value, expression, connection, context):
        if value:
            return value.split(',')
        return []

    def to_python(self, value):
        if isinstance(value, list):
            return value
        return []

    def validate(self, value, model_instance):
        arr_choices = [c[0] for c in self.get_choices(include_blank=False)]
        for opt_select in value:
            if (opt_select not in arr_choices):
                raise exceptions.ValidationError(self.error_messages['invalid_choice'] % value)

    def formfield(self, **kwargs):
        defaults = {'required': not self.blank,
                    'label': self.verbose_name,
                    'help_text': self.help_text,
                    'choices': self.choices,
                    'max_length': self.max_length,
                    'max_choices': self.max_choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)
