from django.db.models import CharField, TextField


class StripCharField(CharField):

    def clean(self, *args):
        value = super(StripCharField, self).clean(*args)
        return value.strip()


class StripTextField(TextField):

    def clean(self, *args):
        value = super(StripTextField, self).clean(*args)
        return value.strip()
